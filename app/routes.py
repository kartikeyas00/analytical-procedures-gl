from flask import render_template, request, redirect, url_for, session, json, jsonify
from app import app
from app.forms import (
    SubmitFile,
    MonthlyEntriesForm,
    UnbalancedEntriesForm,
    WeekendEntriesForm,
    HighDollarEntriesForm,
    SampleJournalEntriesForm,
)
from app.analytical_procedures import *
import pandas as pd


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    basicSubmitform = SubmitFile()
    monthlyEntriesForm = MonthlyEntriesForm()
    weekendEntriesForm = WeekendEntriesForm()
    unbalancedEntriesForm = UnbalancedEntriesForm()
    highDollarEntriesForm = HighDollarEntriesForm()
    sampleJournalEntriesForm = SampleJournalEntriesForm()
    monthlyEntriesForm.months.choices = []
    weekendEntriesForm.weekend.choices = []
    unbalancedEntriesForm.transaction.choices = []
    if basicSubmitform.analyze.data and basicSubmitform.validate_on_submit():
        journal_entry_df = scrub_file(pd.read_excel(basicSubmitform.file.data))
        session["file"] = journal_entry_df
        summary_df = summary(session["file"]).reset_index()
        round_dollar_df = check_round_dollar(session["file"]).reset_index()
        monthlyEntriesForm.months.choices = [
            (i, i)
            for i in pd.to_datetime(session["file"]["Date"]).dt.month_name().unique()
        ]
        weekendEntriesForm.weekend.choices = [
            (i, i)
            for i in session["file"][
                pd.to_datetime(session["file"].Date).dt.dayofweek > 5
            ].Date.unique()
        ]
        unbalancedEntriesForm.transaction.choices = [
            (i, i) for i in session["file"]["Transaction Type"].unique()
        ]
        scatterdata = scatter_data(session["file"])
        scatterdata_credit = {
                'x': scatterdata[2],
                'y': scatterdata[1],
                'mode': 'markers',
                'type': 'scatter'
                }
        scatterdata_debit = {
                'x': scatterdata[2],
                'y': scatterdata[0],
                'mode': 'markers',
                'type': 'scatter'
                }
        return render_template(
            "index.html",
            basicSubmitform=basicSubmitform,
            monthlyEntriesForm=monthlyEntriesForm,
            weekendEntriesForm=weekendEntriesForm,
            unbalancedEntriesForm=unbalancedEntriesForm,
            highDollarEntriesForm=highDollarEntriesForm,
            sampleJournalEntriesForm=sampleJournalEntriesForm,
            summary=json.dumps(summary_df.to_json(orient="records")),
            round_dollar=json.dumps(round_dollar_df.to_json(orient="records")),
            scatterdata_credit=json.dumps(scatterdata_credit),
            scatterdata_debit=json.dumps(scatterdata_debit),
            analyzed=True
        )
    return render_template(
        "index.html",
        basicSubmitform=basicSubmitform,
        monthlyEntriesForm=monthlyEntriesForm,
        weekendEntriesForm=weekendEntriesForm,
        unbalancedEntriesForm=unbalancedEntriesForm,
        highDollarEntriesForm=highDollarEntriesForm,
        sampleJournalEntriesForm=sampleJournalEntriesForm,
        summary=[],
        round_dollar=[],
        scatterdata_credit=[],
        scatterdata_debit=[]
    )


# views below returns json for certain methods from analytical_procedures.py

@app.route("/checkunbalancedentry", methods=["GET", "POST"])
def check_unbalanced_entry_json():
    unbalancedEntriesForm=UnbalancedEntriesForm()
    unbalancedEntriesForm.transaction.choices = [
            (i, i) for i in session["file"]["Transaction Type"].unique()
        ]
    if unbalancedEntriesForm.validate():
        transaction = unbalancedEntriesForm.transaction.data
        df = check_unbalanced_entries(session["file"], transaction)
        print(df)
        df = df.to_json(orient="records")
        return jsonify(df)
    return jsonify('[]')


@app.route("/checkbymonth", methods=["GET", "POST"])
def check_by_month_json():
    monthlyEntriesForm=MonthlyEntriesForm()
    monthlyEntriesForm.months.choices = [
            (i, i)
            for i in pd.to_datetime(session["file"]["Date"]).dt.month_name().unique()
        ]
    if monthlyEntriesForm.validate():
        months = monthlyEntriesForm.months.data
        df = check_by_month(session["file"], months)
        print(df)
        df = df.to_json(orient="records")
        return jsonify(df)
    return jsonify('[]')

@app.route("/checkbyweekend", methods=["GET", "POST"])
def check_by_weekend_json():
    weekendEntriesForm=WeekendEntriesForm()
    weekendEntriesForm.weekend.choices = [
            (i, i)
            for i in session["file"][
                pd.to_datetime(session["file"].Date).dt.dayofweek > 5
            ].Date.unique()
        ]
    if weekendEntriesForm.validate():
        weekend = weekendEntriesForm.weekend.data
        df = check_entries_weekend(session["file"], weekend)
        print(df)
        df = df.to_json(orient="records")
        return jsonify(df)
    return jsonify('[]')

@app.route("/checkhighdollar", methods=["GET", "POST"])
def check_high_dollar_json():
    highDollarEntriesForm=HighDollarEntriesForm()
    if highDollarEntriesForm.validate():
        amount = highDollarEntriesForm.amount.data
        df = check_high_dollar(session["file"], int(amount))
        print(df)
        df = df.to_json(orient="records")
        return jsonify(df)
    return jsonify('[]')

@app.route("/checksample", methods=["GET", "POST"])
def check_sample_json():
    sampleJournalEntriesForm=SampleJournalEntriesForm()
    if sampleJournalEntriesForm.validate():
        number = sampleJournalEntriesForm.number.data
        df = obtain_sample(session["file"], int(number))
        print(df)
        df = df.to_json(orient="records")
        return jsonify(df)
    return jsonify('[]')