from app import db
from app.models.position import Position


class PositionService:
    """
    Production Service Layer
    Handles every database operation
    related to Positions.
    """

    # -----------------------------------------
    # Create Position
    # -----------------------------------------

    @staticmethod
    def create_position(form):

        existing = Position.query.filter(
            Position.election_id == form.election_id.data,
            Position.title.ilike(form.title.data.strip())
        ).first()

        if existing:
            raise ValueError(
                "A position with this title already exists in this election."
            )

        position = Position(
            election_id=form.election_id.data,
            title=form.title.data.strip(),
            description=form.description.data,
            max_candidates=form.max_candidates.data,
            max_votes=form.max_votes.data,
            display_order=form.display_order.data,
            status=form.status.data,
            is_active=form.status.data == "active"
        )

        db.session.add(position)
        db.session.commit()

        return position

    # -----------------------------------------
    # Update Position
    # -----------------------------------------

    @staticmethod
    def update_position(position, form):

        position.election_id = form.election_id.data
        position.title = form.title.data.strip()
        position.description = form.description.data
        position.max_candidates = form.max_candidates.data
        position.max_votes = form.max_votes.data
        position.display_order = form.display_order.data
        position.status = form.status.data
        position.is_active = (
            form.status.data == "active"
        )

        db.session.commit()

        return position

    # -----------------------------------------
    # Archive Position
    # -----------------------------------------

    @staticmethod
    def archive_position(position):

        position.status = "archived"
        position.is_active = False

        db.session.commit()

    # -----------------------------------------
    # Restore Position
    # -----------------------------------------

    @staticmethod
    def restore_position(position):

        position.status = "active"
        position.is_active = True

        db.session.commit()

    # -----------------------------------------
    # Delete Position
    # -----------------------------------------

    @staticmethod
    def delete_position(position):

        db.session.delete(position)
        db.session.commit()

    # -----------------------------------------
    # Position Exists
    # -----------------------------------------

    @staticmethod
    def position_exists(election_id, title):

        return Position.query.filter(
            Position.election_id == election_id,
            Position.title.ilike(title.strip())
        ).first()

    # -----------------------------------------
    # Get Position
    # -----------------------------------------

    @staticmethod
    def get_position(position_id):

        return Position.query.get_or_404(position_id)

    # -----------------------------------------
    # Get All Positions
    # -----------------------------------------

    @staticmethod
    def get_positions():

        return Position.query.order_by(
            Position.display_order.asc(),
            Position.title.asc()
        )

    # -----------------------------------------
    # Search Positions
    # -----------------------------------------

    @staticmethod
    def search(search=None, election_id=None, status=None):

        query = Position.query

        if search:

            query = query.filter(
                Position.title.ilike(
                    f"%{search}%"
                )
            )

        if election_id:

            query = query.filter(
                Position.election_id == election_id
            )

        if status:

            query = query.filter(
                Position.status == status
            )

        return query.order_by(
            Position.display_order.asc(),
            Position.title.asc()
        )

    # -----------------------------------------
    # Statistics
    # -----------------------------------------

    @staticmethod
    def statistics():

        return {

            "total":
            Position.query.count(),

            "active":
            Position.query.filter_by(
                status="active"
            ).count(),

            "inactive":
            Position.query.filter_by(
                status="inactive"
            ).count(),

            "archived":
            Position.query.filter_by(
                status="archived"
            ).count()

        }