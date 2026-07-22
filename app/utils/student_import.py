import os
import pandas as pd

from app import db
from app.models.student import Student
from app.models.faculty import Faculty
from app.models.department import Department
from app.models.program import Program
from app.models.academic_year import AcademicYear
from app.models.semester import Semester
from app.utils.student_id import (
    generate_student_id,
    generate_roll_number
)


# ==========================================
# Required Columns
# ==========================================

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


# ==========================================
# Template Validation
# ==========================================

def validate_template(df):

    missing = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    return missing


# ==========================================
# Read CSV or Excel
# ==========================================

def read_import_file(file_path):

    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.csv':

        return pd.read_csv(file_path)

    elif ext in ['.xlsx', '.xls']:

        return pd.read_excel(file_path)

    else:

        raise ValueError(
            'Unsupported file format. Use .csv or .xlsx'
        )


# ==========================================
# Main Import Function
# ==========================================

def import_students(file_path):

    result = {
        'success': 0,
        'failed': 0,
        'errors': []
    }

    try:

        # Read file
        df = read_import_file(file_path)

        # Normalize column names
        df.columns = [
            col.strip().lower()
            for col in df.columns
        ]

        # Validate template
        missing_columns = validate_template(df)

        if missing_columns:

            result['errors'].append(
                f'Missing columns: {", ".join(missing_columns)}'
            )

            return result

        # Process rows
        for index, row in df.iterrows():

            row_number = index + 2

            try:

                # Skip empty rows
                if pd.isna(row['email']):
                    continue

                email = str(row['email']).strip().lower()

                # Duplicate check
                existing = Student.query.filter_by(
                    email=email
                ).first()

                if existing:

                    result['failed'] += 1

                    result['errors'].append(
                        f'Row {row_number}: Email already exists ({email})'
                    )

                    continue

                # Find academic hierarchy
                faculty = Faculty.query.filter_by(
                    name=str(row['faculty']).strip(),
                    is_active=True
                ).first()

                department = Department.query.filter_by(
                    name=str(row['department']).strip(),
                    is_active=True
                ).first()

                program = Program.query.filter_by(
                    name=str(row['program']).strip(),
                    is_active=True
                ).first()

                academic_year = AcademicYear.query.filter_by(
                    name=str(row['academic_year']).strip(),
                    is_active=True
                ).first()

                semester = Semester.query.filter_by(
                    name=str(row['semester']).strip(),
                    is_active=True
                ).first()

                # Validate relationships
                if not faculty:
                    raise ValueError('Faculty not found')

                if not department:
                    raise ValueError('Department not found')

                if not program:
                    raise ValueError('Program not found')

                if not academic_year:
                    raise ValueError('Academic Year not found')

                if not semester:
                    raise ValueError('Semester not found')

                # Validate department belongs to faculty
                if department.faculty_id != faculty.id:
                    raise ValueError(
                        'Department does not belong to selected faculty'
                    )

                # Validate program belongs to department
                if program.department_id != department.id:
                    raise ValueError(
                        'Program does not belong to selected department'
                    )

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

                    email=email,
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
                    f'Row {row_number}: {str(e)}'
                )

        # Commit all valid rows
        db.session.commit()

    except Exception as e:

        db.session.rollback()

        result['errors'].append(
            f'Import failed: {str(e)}'
        )

    return result