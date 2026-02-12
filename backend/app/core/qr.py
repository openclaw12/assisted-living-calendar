import base64
import io

import segno


def generate_qr_data_uri(data: str) -> str:
    qr = segno.make(data)
    buf = io.BytesIO()
    qr.save(buf, kind="png", scale=4)
    encoded = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"
