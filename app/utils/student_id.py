from app.models.program import Program
from app.models.student import Student


def generate_student_id(program_id: int, admission_year: int) -> str:
    """
    Generate student ID like: BIT-2026-0001
    """

    program = Program.query.get(program_id)

    if not program:
        raise ValueError("Invalid Program ID")

    prefix = program.code.upper()

    existing_count = Student.query.filter_by(
        program_id=program_id,
        admission_year=admission_year
    ).count()

    sequence = existing_count + 1

    return f"{prefix}-{admission_year}-{sequence:04d}"


def generate_roll_number(program_id: int, admission_year: int) -> str:
    """
    Generate roll number like: 2026BIT001
    """

    program = Program.query.get(program_id)

    if not program:
        raise ValueError("Invalid Program ID")

    prefix = program.code.upper()

    existing_count = Student.query.filter_by(
        program_id=program_id,
        admission_year=admission_year
    ).count()

    sequence = existing_count + 1

    return f"{admission_year}{prefix}{sequence:03d}"