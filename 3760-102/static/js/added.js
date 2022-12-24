'use strict'

// component for creating tables in schedule tab, with the added courses 
class AddedTables extends React.Component{
    constructor(props){
      super(props);
      this.state = {
        courseF:'',
        courseW:'',
        empty: false
      };
    
      //binding so arguments can be passed between functions
      this.createAdded = this.createAdded.bind(this);
      this.handleDelete = this.handleDelete.bind(this);
      this.createNoTime = this.createNoTime.bind(this);
      this.getAdded = this.getAdded.bind(this);
      this.checkOverlap = this.checkOverlap.bind(this);
    }
  
    // table for added courses is rendered every second
    componentDidMount() {
      // Call this function so that it fetch first time right after mounting the component
      this.getAdded();
  
      // set Interval
      this.interval = setInterval(this.getAdded, 1000);
    }
  
    componentWillUnmount() {
        // Clear the interval right before component unmount
        clearInterval(this.interval);
    }
    
    // get the added courses 
    getAdded(){
        // console.log(addedClass);

        if(addedClass){
            let jsonF = jsonClassesF;
            let jsonW = jsonClassesW;
            
            this.setState({
                courseF: jsonF,
                courseW: jsonW
            });
        }else{
            this.setState({
                empty: true
            });
        }
        addedClass=false;
    }
  
  
    // delete the course from text.json, send back the file data, createAdded should automatically display it
    handleDelete(event, selected){
        // console.log(selected.title);

        $.ajax({
            type:'DELETE',
            url: "/deleteJSON",
            data: {
                title: selected.title
            },
            success: function(result){ 
    
            }.bind(this)
        });
        
        if (semCal == "F22") {
            let temp = jsonClassesF;
            let filteredTmp = temp.filter(function(temp){
                return temp.title != selected.title;
            });

            jsonClassesF = filteredTmp;

            calendar.getEventById(selected.id).remove();
            calendar.getEventById(selected.id + " Lab").remove();

            this.setState({
                courseF: jsonClassesF
            });
        }
        if (semCal == "W23") { 
            let temp = jsonClassesW;
            let filteredTmp = temp.filter(function(temp){
                return temp.title != selected.title;
            });

            jsonClassesW = filteredTmp;

            winterCalendar.getEventById(selected.id).remove();
            winterCalendar.getEventById(selected.id + " Lab").remove();

            this.setState({
                courseW: jsonClassesW
            });
        }
    
    };
    
    // check if courses added are overlapping in times
    checkOverlap(selectedCourse){
        let overlap = false;
        let courses = "";
        if (semCal == "F22") { // Add fall courses to table if fall calendar is chosen
            courses = this.state.courseF;
        }
        else if (semCal == "W23") {
            courses = this.state.courseW;
        }
    
        if(courses.length > 1){
            // let newDays = selectedCourse.daysOfWeek;
            let newDays = selectedCourse.lecDays;
            // console.log("new days");
            newDays = newDays.split(',');
            // console.log(newDays[0]);
    
            let nLecStart = selectedCourse.startTime;
            let nLecEnd = selectedCourse.endTime;
    
            nLecStart = nLecStart.replace(':', '.');
            nLecEnd = nLecEnd.replace(':', '.');

            // console.log("new lec");
            // console.log(nLecStart);
            // console.log(nLecEnd);

            
            let nLabDay = selectedCourse.labDay;
    
            let nLabStart = selectedCourse.lab_sTime;
            nLabStart = nLabStart.replace(':', '.');
    
            let nLabEnd = selectedCourse.lab_eTime;
            nLabEnd = nLabEnd.replace(':', '.');

            // console.log("new lab");
            // console.log(nLabStart);
            // console.log(nLabEnd);
    
            courses.forEach((course) => {
                // let oldDays = course.daysOfWeek;
                if(selectedCourse.title != course.title ){
                    let oldDays = course.lecDays;
                    oldDays = oldDays.split(',');
            
                    let sameDay = false;
                    let oLecStart = course.startTime;
                    let oLecEnd = course.endTime;
            
                    oLecStart = oLecStart.replace(":" , ".");
                    oLecEnd = oLecEnd.replace(":" , ".");

                    // console.log("o lec");
                    // console.log(oLecStart);
                    // console.log(oLecEnd);

                    let oLabDay = course.labDay;
            
                    let oLabStart = course.lab_sTime;
                    oLabStart = oLabStart.replace(':' , '.');
            
                    let oLabEnd = course.lab_eTime;
                    oLabEnd = oLabEnd.replace(':' , '.');

                    // console.log("o lab");
                    // console.log(oLabStart);
                    // console.log(oLabEnd);
        
                    // #if lecture days exist in both courses from file and selected course
                    // #compare days of the week
                    if(newDays[0] != "TBA" && oldDays[0] != "TBA"){
                        newDays.forEach((nDay) =>{
                            oldDays.forEach((oDay) =>{
                
                                // #get rid of white space and check if they have same days
                                nDay = nDay.replace(/\s\s+/g, ' ');
                                oDay = oDay.replace(/\s\s+/g, ' ');
                                if(nDay == oDay ){
                                    sameDay = true;
                                    // console.log("same");
                                }
                            });
                        });
                        
            
                        // #if day is same between courses check times
                        if(sameDay == true){
                            if(parseFloat(oLecStart) <= parseFloat(nLecEnd) && parseFloat(oLecEnd) >= parseFloat(nLecStart)){
                                overlap = true;
                            }else if(parseFloat(nLecStart) <= parseFloat(oLecEnd) && parseFloat(nLecEnd) >= parseFloat(oLecStart)){
                                overlap = true;
                            }

                            // console.log("#1");
                            // console.log(overlap);
                        }
                        
                        // # check conflict between labs (labs can't occur without there being lecutres)
                        if(overlap == false){
                            sameDay = false;
                            
                            // #if both have labs
                            if(nLabDay != "" && oLabDay != ""){
                                if(nLabDay == oLabDay){
                                    sameDay = true;
                                }
                            }
                
                            // #lab on the same day
                            if (sameDay == true){
                                if(parseFloat(oLabStart) <= parseFloat(nLabEnd) && parseFloat(oLabEnd) >= parseFloat(nLabStart)){
                                    overlap = true;
                                }else if(parseFloat(nLabStart) <= parseFloat(oLabEnd) && parseFloat(nLabEnd) >= parseFloat(oLabStart)){
                                    overlap = true;
                                }

                                // console.log("#2");
                                // console.log(overlap);
                            }
            
                        }
        
                        // #2 check conflict between course in file lecture time from with added course lab time
                        if(overlap == false){
                            // if(nLabDay != ""){
                                sameDay = false;
                            // }
                
                            // #compare lecture days with lab day
                            oldDays.forEach((oDay) => {
                                oDay = oDay.replace(/\s\s+/g, ' ');
                                if(oDay == nLabDay){
                                    sameDay = true;
                                }
                            });
                            
                        
                            // #check time if on same day
                            if(sameDay == true){
                                if(parseFloat(oLecStart) <= parseFloat(nLabEnd) && parseFloat(oLecEnd) >= parseFloat(nLabStart)){
                                    overlap = true;
                                    // console.log("3.1");
                                }

                                // console.log("#3");
                                // console.log(overlap);
                            }
                            
                        }

                        if (overlap == false){
                            // if (oLabDay != ""){
                                sameDay = false;
                            // }
            
                            // #compare lecture days with lab day
                            newDays.forEach((nDay) =>{
                                if(nDay.trim() == oLabDay){
                                    sameDay = true;
                                    // console.log(nDay);
                                    // console.log(oLabDay);
                                    // console.log("same 4");
                                }
                            });
                            
                        
                            // #check time if on same day
                            if(sameDay == true){
                                if(parseFloat(oLabStart) <= parseFloat(nLecEnd) && parseFloat(oLabEnd) >= parseFloat(nLecStart)){
                                    overlap = true;
                                    // console.log("here1");
                                }
                                // console.log("#4");
                                // console.log(overlap);
                            }
                            
                        }

                
                    }
                }
                
            });
        }
        return (overlap);
    }
  
    // create table with added courses with remove button next to each name 
    createAdded(){
        // console.log("not empty");

        //only add in the lecture names to table
        let courses = this.state.courseF;
        if (semCal == "F22") { // Add fall courses to table if fall calendar is chosen
            courses = this.state.courseF;
        }
        else if (semCal == "W23") {
            courses = this.state.courseW;
        }
        let totalCredits = 0;
        Array.from(courses).map((t, index) => {
            totalCredits += parseFloat(t.credit);
        });

        return(
            <div className="pb-5">
            <table className="table text-white px-2 table-wrapper2" style={{textAlign:"center"}}>
            <thead>
                <tr>
                  <th>Added Courses {semCal}</th>
                  <th>
                  </th>
                </tr>
            </thead>
            <tbody>
            {/* table has 2 rows, course name and remove /*/}
            {Array.from(courses).map((t, index) =>
              <tr key={index} style ={this.checkOverlap(t) ? {backgroundColor: "#bf4846"} : {}}>
                <td style={{fontSize:"15px"} }>{t.title}</td>
                <td>
                  {/* send the handle delete function the entire json format of the selected course */}
                  <button type="button"  className="btn btn-warning btn-sm" onClick={(event)=> {this.handleDelete(event, t)}}>
                    Remove
                  </button>
                </td>
  
              </tr>
            )}
  
            </tbody>
            </table>

            <div>
                Total Credits: {totalCredits}
            </div>
          </div>
  
        );
    } 
   
  
  
    // create table with courses without a meeting time in seperate table
    createNoTime(){
        let hasTBA = false;
        let tba = [];
        
        let courses = this.state.courseF;
        if (semCal == "F22") {
            courses = this.state.courseF;
        }
        if (semCal == "W23") {
            courses = this.state.courseW;
        }
        // console.log("no time");
        
        // save the courses that have no lecture meeting time (time = "TBA") in list
        Array.from(courses).map((t, index) => {
            if(t.daysOfWeek.length == 0){
                // console.log("TBA");
                tba.push(t.title);
                hasTBA = true;
            }
        });
        
        // console.log(tba);
        // go through list and display the table 
        if(hasTBA == true){
            return(
            <div className="mt-5 pb-5 table-wrapper2">
                <table className="table text-white px-2" style={{textAlign:"center"}}>
                <thead>
                    <tr>
                    <th style={{fontSize:"15px"}}>Courses Without Meeting Times</th>
                    </tr>
                </thead>
                <tbody>
                {/* t is course name */}
                {tba.map((t, index) => 
                    <tr key={index}>
                        <td style={{fontSize:"15px"}}>{t}</td>
                    </tr>
                )}
            
                </tbody>
                </table>
            </div>
            );
        }
    }
  
    render(){
        return(
            <div>
                {this.createAdded()}
                {this.createNoTime()}
            </div>
        );
    }
}




const addedTables = document.getElementById('addedTables');
const root2 = ReactDOM.createRoot(addedTables);
root2.render(<AddedTables/>);
