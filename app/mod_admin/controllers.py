from app.models.Permission import roles
from app.decorators import permission_required


@permission_required(roles['admin'][0])
def admin():
    """The admin panel."""

    return 'hello admin'
