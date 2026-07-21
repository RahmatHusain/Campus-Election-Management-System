import pandas as pd
from app import db
from app.models.student import Student
from app.models.faculty import Faculty
from app.models.department import Department
from app.models.program import Program
from app.models.academic_year import AcademicYear
from app.models.semester import Semester
from app.utils.student_id import generate_student_id, generate_roll_number


REQUIRED_COLUMNS = [
    'first_name',
    'last_name',
    'gender',
    'date_of_birth',
    'email',
    'phone',
    'faculty',
    'department',
    'program',
    'academic_year',
    'semester',
    'admission_year'
]


def validate_template(df):
    missing = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    return missing


def import_students_from_excel(file_path):

    result = {
        'success': 0,
        'failed': 0,
        'errors': []
    }

    df = pd.read_excel(file_path)

    # Validate template
    missing_columns = validate_template(df)

    if missing_columns:
        result['errors'].append(
            f'Missing columns: {", ".join(missing_columns)}'
        )
        return result

    for index, row in df.iterrows():

        try:

            # Skip empty rows
            if pd.isna(row['email']):
                continue

            # Duplicate email check
            existing = Student.query.filter_by(
                email=str(row['email']).strip().lower()
            ).first()

            if existing:
                result['failed'] += 1
                result['errors'].append(
                    f'Row {index + 2}: Email already exists'
                )
                continue

            # Find relationships
            faculty = Faculty.query.filter_by(
                name=str(row['faculty']).strip()
            ).first()

            department = Department.query.filter_by(
                name=str(row['department']).strip()
            ).first()

            program = Program.query.filter_by(
                name=str(row['program']).strip()
            ).first()

            academic_year = AcademicYear.query.filter_by(
                name=str(row['academic_year']).strip()
            ).first()

            semester = Semester.query.filter_by(
                name=str(row['semester']).strip()
            ).first()

            if not all([
                faculty,
                department,
                program,
                academic_year,
                semester
            ]):
                result['failed'] += 1
                result['errors'].append(
                    f'Row {index + 2}: Invalid academic hierarchy'
                )
                continue

            admission_year = int(row['admission_year'])

            # Generate IDs
            student_id = generate_student_id(
                program.id,
                admission_year
            )

            roll_number = generate_roll_number(
                program.id,
                admission_year
            )

            # Create student
            student = Student(
                student_id=student_id,
                roll_number=roll_number,

                first_name=str(row['first_name']).strip(),
                last_name=str(row['last_name']).strip(),
                gender=str(row['gender']).strip(),
                date_of_birth=pd.to_datetime(
                    row['date_of_birth']
                ).date(),

                email=str(row['email']).strip().lower(),
                phone=str(row['phone']).strip(),

                faculty_id=faculty.id,
                department_id=department.id,
                program_id=program.id,
                academic_year_id=academic_year.id,
                semester_id=semester.id,

                admission_year=admission_year,

                is_voter=True,
                is_verified=False,
                is_active=True
            )

            db.session.add(student)

            result['success'] += 1

        except Exception as e:

            result['failed'] += 1

            result['errors'].append(
                f'Row {index + 2}: {str(e)}'
            )

    # Commit all successful rows
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        result['errors'].append(
            f'Database commit failed: {str(e)}'
        )

    return result