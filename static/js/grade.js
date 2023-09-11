const numCourses = document.getElementById("numCourses");
const subjects_div = document.getElementById("subjects");
const numCoursesMsg = document.getElementById("numCoursesMsg");
const form = document.getElementById("form");

numCourses.addEventListener('keyup',event => getSubjects(event.target.value))
function getSubjects(num) {
    subjects_div.innerHTML = numCoursesMsg.innerHTML = '';
    if (num>4) {
        numCoursesMsg.innerHTML=`Subject count can't be greater than 4`;
    } else if(num<1) {
        numCoursesMsg.innerHTML=`Subject count can't be less than 1`;
    }
    else{
    for (let index = 1; index <= num; index++) {
        subjects_div.innerHTML+= `
        <div class='mb-3'>
            <fieldset>
                <legend>For Subject ${index}</legend>
                    <div class="form-floating mb-1">
                        <input type="text" class="form-control" id="sub${index}_name" name="sub${index}_name" placeholder="Name of Subject ${index}"/>
                        <label for="sub${index}_name">Name of Subject ${index}</label>
                    </div>
                    <div class="form-floating mb-1">
                        <input type="number" min="1" max="100" step="0.01" class="form-control" id="sub${index}_qz1" name="sub${index}_qz1" placeholder="Quiz 1 Score" required/>
                        <label for="sub${index}_qz1">Quiz 1 Score</label>
                    </div>
                    <div class="form-floating mb-1">
                        <input type="number" min="1" max="100" step="0.01" class="form-control" id="sub${index}_qz2" name="sub${index}_qz2" placeholder="Quiz 2 Score" required/>
                        <label for="sub${index}_qz2">Quiz 2 Score</label>
                    </div>
                    <div class="form-floating mb-1">
                        <input type="number" min="1" max="100" step="0.01" class="form-control" id="sub${index}_et" name="sub${index}_et" placeholder="End Term Score" required/>
                        <label for="sub${index}_et">End Term Score</label>
                    </div>
                    <div class="form-floating mb-1">
                        <input type="number" min="1" max="100" step="0.01" class="form-control" id="sub${index}_agas" name="sub${index}_agas" placeholder="Average Graded Assignment Score" required/>
                        <label for="sub${index}_agas">Average Graded Assignment Score</label>
                    </div>
                    <div class="form-floating mb-1">
                        <input type="number" min="0" max="5" step="0.01" class="form-control" id="sub${index}_pab" name="sub${index}_pab" placeholder="Practice Assignment Bonus" required/>
                        <label for="sub${index}_pab">Practice Assignment Bonus</label>
                    </div>
            </fieldset>
        </div>
        `;
    }
}
}
