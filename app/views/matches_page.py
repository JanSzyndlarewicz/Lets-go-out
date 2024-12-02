from flask import Blueprint, redirect, render_template, url_for

from app.models.user import User
from app.views.auth import confirmed_required
from flask_login import current_user

matches_page_bp = Blueprint("matches_page_bp", __name__)


@matches_page_bp.route("/matches-page")
@confirmed_required
def matches_page():
    return redirect(url_for("matches_page_bp.matches_page_proposed"))

@matches_page_bp.route("/matches-page/proposed")
@confirmed_required
def matches_page_proposed():
    proposed_and_ignored = current_user.profile.proposed_and_ignored_proposals_by_self
    
    return render_template(
        "main/matches_page.html", 
        proposals_data=proposed_and_ignored, 
        redirect_buttons_set_data=redirect_buttons_set_data()
        )

@matches_page_bp.route("/matches-page/accepted")
@confirmed_required
def matches_page_accepted():
    
    return render_template("main/matches_page.html")

@matches_page_bp.route("/matches-page/rejected")
@confirmed_required
def matches_page_rejected():
    
    return render_template("main/matches_page.html")

@matches_page_bp.route("/matches-page/reschedule")
@confirmed_required
def matches_page_reschedule():
    
    return render_template("main/matches_page.html")

def redirect_buttons_set_data():
    return [{"url": url_for("matches_page_bp.matches_page_proposed"), "text": "proposed"}, 
            {"url": url_for("matches_page_bp.matches_page_accepted"), "text": "accepted"},
            {"url": url_for("matches_page_bp.matches_page_rejected"), "text": "rejected"},
            {"url": url_for("matches_page_bp.matches_page_reschedule"), "text": "reschedule"}]
    