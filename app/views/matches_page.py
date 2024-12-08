from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user

from app.models.user import User
from app.views.auth import confirmed_required

matches_page_bp = Blueprint("matches_page_bp", __name__)


@matches_page_bp.route("/matches-page")
@confirmed_required
def matches_page():
    return redirect(url_for("matches_page_bp.matches_page_sent"))


@matches_page_bp.route("/matches-page/sent")
@confirmed_required
def matches_page_sent():
    sent_by_self = current_user.profile.proposals_sent_by_self
    return render_template(
        "main/matches_page.html",
        proposals_data=sent_by_self,
        redirect_buttons_set_data=redirect_buttons_set_data(),
        active_nav="matches",
    )


@matches_page_bp.route("/matches-page/received")
def matches_page_received():
    proposals_considered_by_self = current_user.profile.proposals_considered_by_self
    return render_template(
        "main/matches_page.html",
        proposals_data=proposals_considered_by_self,
        redirect_buttons_set_data=redirect_buttons_set_data(),
        active_nav="matches",
    )


@matches_page_bp.route("/matches-page/dates")
@confirmed_required
def matches_page_dates():
    accepted_by_either = current_user.profile.accepted_proposals_by_either
    return render_template(
        "main/matches_page.html",
        proposals_data=accepted_by_either,
        redirect_buttons_set_data=redirect_buttons_set_data(),
        active_nav="matches",
    )


def redirect_buttons_set_data():
    return [
        {"url": url_for("matches_page_bp.matches_page_sent"), "text": "sent"},
        {"url": url_for("matches_page_bp.matches_page_received"), "text": "received"},
        {"url": url_for("matches_page_bp.matches_page_dates"), "text": "dates"},
    ]
