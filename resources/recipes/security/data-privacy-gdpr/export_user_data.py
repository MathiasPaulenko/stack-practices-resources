"""GDPR Article 20 data portability export.

Produces a ZIP containing all personal data for a user in JSON.
"""

import json
from datetime import datetime, timezone
from io import BytesIO
from zipfile import ZipFile


def export_user_data(user_id: str, db) -> bytes:
    """Export all personal data for a user as a ZIP with JSON files."""
    data = {
        'profile': db.get_user_profile(user_id),
        'orders': db.get_user_orders(user_id),
        'consents': db.get_user_consents(user_id),
        'activity_logs': db.get_user_activity(user_id),
    }

    # Remove internal fields and keep only personal data
    for section in data.values():
        if isinstance(section, list):
            for item in section:
                item.pop('id', None)
                item.pop('internal_status', None)
        elif isinstance(section, dict):
            section.pop('id', None)

    export = {
        'user_id': user_id,
        'exported_at': datetime.now(timezone.utc).isoformat(),
        'format': 'GDPR Article 20 Data Portability',
        'data': data,
    }

    json_bytes = json.dumps(export, indent=2, default=str).encode('utf-8')

    buffer = BytesIO()
    with ZipFile(buffer, 'w') as zf:
        zf.writestr('user_data.json', json_bytes)

    return buffer.getvalue()


# Usage in Flask
# @app.route('/api/gdpr/export', methods=['POST'])
# @require_auth
# def request_export():
#     user_id = request.user.id
#     data = export_user_data(user_id, db)
#     return send_file(
#         BytesIO(data),
#         mimetype='application/zip',
#         as_attachment=True,
#         download_name=f'gdpr_export_{user_id}.zip'
#     )
