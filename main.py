from flask import Flask, render_template, request, redirect
import os
from deta import Deta
from cgpa import CalculateTotalScore
import collections

app = Flask(__name__)

def marks_required(quiz1:float,quiz2:float):
    weighted_quiz1 = 0.2 * quiz1
    weighted_quiz2 = 0.3 * quiz2
    total_weighted_marks = weighted_quiz1 + weighted_quiz2
    if quiz2 > quiz1:
        weighted_quiz2 = 0.2 * quiz2
    else:
        weighted_quiz1 = 0.2 * quiz1
    required_marks = 40 - total_weighted_marks
    return round(required_marks/0.4,2)

def new_view():
    project_key = os.environ.get('DETA_PROJECT_KEY')
    if project_key is not None:
        deta = Deta(project_key)
        base = deta.Base('visitors')
        visitors = base.get('visitor_count')
        count = 0
        if type(visitors) is dict:
            count = visitors['value'] + 1
            base.put(count,key='visitor_count')
        else:
            count+=1
            base.put(count,key='visitor_count')
        return count
    else:
        return 0

@app.route('/',methods=['GET'])
def index():
    count = new_view()
    return render_template('index.html',visitors=count)

@app.route('/grade',methods=['GET','POST'])
def grade():
    count = new_view()
    if request.method=='POST':
        form_data = request.form
        num_courses = int(form_data.get('num_courses',0))
        Course = collections.namedtuple('Course',['subject','quiz1','quiz2','endterm','gaa','pa_bonus'])
        marks_list = [
                    Course(str(request.form.get(f'sub{i}_name')) if str(request.form.get(f'sub{i}_name')) != '' else f'Subject {i}',
                             float(form_data.get(f'sub{i}_qz1')),
                             float(form_data.get(f'sub{i}_qz2')),
                             float(form_data.get(f'sub{i}_et')),
                             float(form_data.get(f'sub{i}_agas')),
                             float(form_data.get(f'sub{i}_pab'))
                             ) \
                      for i in range(1,num_courses+1)
                      ]
        grades = []
        gpa=0
        for item in marks_list:
            score = CalculateTotalScore(item.endterm,
                                        item.quiz1,
                                        item.quiz2,
                                        item.gaa,
                                        item.pa_bonus
                                        )
            best_score = score.best_score
            total = best_score + item.pa_bonus if best_score <= 95 else best_score
            grade,point = score.get_grade(total)
            gpa+=point
            grades.append({'subject':item.subject,'total_score':round(total,2),'grade':grade,'point':point})
        return render_template('grades-table.html',subjects=grades,visitors=count,gpa=round(gpa/num_courses,2))
    else:
        return render_template('grade.html',visitors=count)

@app.route('/endterm',methods=['GET'])
def endterm():
    count = new_view()
    return render_template('endterm.html',data={'calculated':False},visitors=count)

@app.route('/calculate',methods=['GET'])
def calculate():
    count = new_view()
    name = request.args.get('name', 'Anonymous')
    try:
        quiz1 = float(request.args['quiz1'])
        quiz2 = float(request.args['quiz2'])
    except:
        return redirect('/')
    required_marks= marks_required(quiz1,quiz2)
    data = {
        'calculated' : True,
        'marks_required' : required_marks,
        'quiz1' : quiz1,
        'quiz2' : quiz2,
        'name' : name
    }
    return render_template('endterm.html',data=data,visitors=count)

if __name__=='__main__':
    app.run(debug=True,port=os.environ.get('PORT',5000))