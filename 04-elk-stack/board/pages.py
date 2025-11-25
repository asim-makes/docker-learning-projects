from flask import Blueprint, render_template, current_app


bp = Blueprint("pages", __name__)

@bp.route("/")
def home():
    current_app.logger.info("Home page accessed successfully.", extra={'route': '/'})
    return render_template("pages/home.html")

@bp.route("/about")
def about():
    try:
        raise ValueError("Simulated backend issue.")
    except Exception as e:
        current_app.logger.error(f"Error accessing about page: {str(e)}",
                                 extra={'route': '/about', 'error_type': type(e).__name__})

    return render_template("pages/about.html")
