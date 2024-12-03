from flask import Blueprint, jsonify, render_template, url_for
from flask_login import current_user

from app.views.auth import confirmed_required

you_page_bp = Blueprint("you_page_bp", __name__)


@you_page_bp.route("/you-page")
@confirmed_required
def you_page():
    liked = current_user.liking
    return render_template("main/you_page.html", users=liked, pull_buttons_set_data=pull_buttons_set_data(), active_nav="you")

@you_page_bp.route("/sub-you-page-liked")
@confirmed_required
def sub_you_page_liked():
    liked = current_user.liking
    if not liked:
        return jsonify({"html": render_template("components/this_list_is_empty.html")})
    return jsonify({"html": render_template("components/users_profile_briefs.html", users=liked)})

@you_page_bp.route("/sub-you-page-blocked")
@confirmed_required
def sub_you_page_blocked():
    blocked = current_user.blocking
    if not blocked:
        return jsonify({"html": render_template("components/this_list_is_empty.html")})
    return jsonify({"html": render_template("components/users_profile_briefs.html", users=blocked)})

def pull_buttons_set_data():
    return [{"jsCallBackIndicator": "switch-to-liked", "text": "liked"}, 
            {"jsCallBackIndicator": "switch-to-blocked" , "text": "blocked"},]
    
    