from flask import Blueprint, url_for, render_template, request, flash, redirect
from flask_login import login_required, current_user
from .model import User,Workout, db

main_bp=Blueprint("main_bp",__name__)

@main_bp.route("/")
def home():
    return render_template('index.html')

@main_bp.route("/account")
@login_required
def profile():
    page=request.args.get('page',1,type=int)
    user=User.query.filter_by(email=current_user.email).first()
    workout=Workout.query.filter_by(author=user).paginate(page=page, per_page=3)
    return render_template('profile.html',name=current_user.name, workouts=workout, user=user)

@main_bp.route("/create_workout", methods=["POST","GET"])
@login_required
def create_workout():
    if request.method == "POST":
        pushups=request.form.get('pushups')
        comment=request.form.get('comment')
        workout=Workout(pushups=pushups, comment=comment, author=current_user)
        db.session.add(workout)
        db.session.commit()
        print(workout)
        flash("New workout added")
        return redirect(url_for('main_bp.profile'))
    return render_template('create_workout.html',name=current_user.name)

@main_bp.route("/workout/<int:workout_id>/update", methods=["POST","GET"])
@login_required
def update_workout(workout_id):
    print(workout_id)
    workouts=Workout.query.filter_by(id=workout_id).first()
    if request.method=="POST":
        workouts.pushups=request.form.get('pushups')
        workouts.comment=request.form.get('comment')
        db.session.commit()
        flash("Workout Updated")
        return redirect(url_for('main_bp.profile'))
    return render_template('update_workout.html', workout=workouts)

@main_bp.route("/workout/<int:workout_id>/delete", methods=["POST","GET"])
@login_required
def delete_workout(workout_id):
    print(workout_id)
    workouts=Workout.query.filter_by(id=workout_id).first()
    db.session.delete(workouts)
    db.session.commit()
    flash("Workout Deleted")
    return redirect(url_for('main_bp.profile'))
