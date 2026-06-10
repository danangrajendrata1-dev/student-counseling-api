import math


def normalize_pagination(page: int, limit: int) -> tuple[int, int, int]:
    safe_page = max(page, 1)
    safe_limit = min(max(limit, 1), 100)
    offset = (safe_page - 1) * safe_limit

    return safe_page, safe_limit, offset


def build_pagination_meta(page: int, limit: int, total: int) -> dict:
    total_pages = math.ceil(total / limit) if total > 0 else 0

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
    }