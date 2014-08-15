from app.decorators import permission_required
from app.models.user.Permission import roles


@permission_required(roles['admin'][0])
def admin():
    """The admin panel."""

    return 'hello admin'
