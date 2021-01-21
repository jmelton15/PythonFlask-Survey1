from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
import json
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "SUPER-SECRET-CODE"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False #set to true if you want to debug
debug = DebugToolbarExtension(app) #app bcs app name is app

responses = []
page_number = 0



@app.route('/', methods=["GET","POST"])
#@app.route('/survey_page', methods=["GET","POST"])
def survey_page():
    """Landing Page for the surveys. Uses session data for page number and responses.
    Responses and page_number should reset back to their initial values when visiting home page
    """
    #session.clear()
    survey_title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    session["p_num"] = page_number
    session["responses"] = responses
    return render_template("main.html",survey_title=survey_title,instructions=instructions)



@app.route(f'/questions/<int:page>', methods=["GET","POST"])
def show_questions_page(page):
    """[I use a session variable called page_numbers that is set to the value of the "page"
        or url parameter. Initially page and page_number are 0. This function has checks for 
        if and how many responses a user has submitted and responds accordingly. Will either redirect
        or render a new form based on if the session was a POST or GET request. This function will also
        make sure a choice is selected and will not allow a user to skip to different questions before completing
        the survey questions]
    """
    responses = session.get("responses")
    if len(responses) < page:
        flash("You Must First Answer The Question On This Page Before Continuing", "error")
        return redirect(f'/questions/{len(responses)}')
    if page > len(satisfaction_survey.questions) -1:
        return redirect("/thanks")
    if request.method == "POST":
        choice = request.form.get("flexRadioDefault")
        if choice:
            if len(responses) < len(satisfaction_survey.questions):
                responses.append(choice)
                session["responses"] = responses
            return redirect("/answers")
        else:
            flash("Please Select An Answer Before Pressing Next", "error")
            return redirect(f"/questions/{page}")
    else:
        session["p_num"] = page
        question = satisfaction_survey.questions[page].question
        choices = satisfaction_survey.questions[page].choices
        return render_template("questions.html",question=question,choices=choices)
    
    
@app.route("/answers")
def go_next_question():
    """[This page only happens behind the scenes and is used to increment the page number for my session variable]
    """
    page_number = session.get("p_num")
    page_number+=1
    return redirect(f"questions/{page_number}")

@app.route("/thanks", methods=["GET","POST"])
def show_thanks():
    """Thank you Page for completing survey
    """
    responses = session.get("responses")
    flash("Thank You For Taking The Time To Complete Our Survey!", 'success')
    return render_template("thanks.html",responses=responses)


   
