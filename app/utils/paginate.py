import math

def paginate_query(data, page=1, per_page=10):
    from flask import request

    page = int(request.args.get("page", page))
    per_page = int(request.args.get("per_page", per_page))

    if hasattr(data, "paginate"): 
        paginated = data.paginate(page=page, per_page=per_page, error_out=False)
        items = [item.to_dict() for item in paginated.items]
        total = paginated.total
        pages = paginated.pages
    else:  
        total = len(data)
        pages = math.ceil(total / per_page) if total > 0 else 0
        start = (page - 1) * per_page
        end = start + per_page
        items = data[start:end]

    return {
        "total": total,
        "pages": pages,
        "current_page": page,
        "per_page": per_page,
        "items": items
    }