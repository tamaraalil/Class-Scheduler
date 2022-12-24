'use strict';
const {OverlayTrigger, Tooltip, Button, Popover, DropdownButton, Dropdown, Col, Form, Overlay} = ReactBootstrap;


var jsonClassesF = []; //storing only the non lab classes (using for added tables)
var jsonClassesW = []; //storing only the non lab classes (using for added tables)
var selectedDay = [];
var selectedLab = [];
var addedClass = false;
var semester = "";
var semCal = "";
var selectedSemester = "F22";

class Search extends React.Component{

  //intializing the state with searchFor (user input) and classes (output) to be empty
  constructor(props){
    super(props);
    this.state = {
      searchFor:'',
      clicked:false,
      empty:false,
      badcourse:false,
      table:'',
      semester:'F22',
      day:["None"],
      lab:["None"]
    }

    //binding so arguments can be passed between functions
    this.handleChange = this.handleChange.bind(this);
    this.showSearchResults = this.showSearchResults.bind(this);
    this.handleAdd = this.handleAdd.bind(this);
    this.added = React.createRef();
    this.handleSelect = this.handleSelect.bind(this);
    this.handleDaySelect = this.handleDaySelect.bind(this);
    this.handleLabDaySelect = this.handleLabDaySelect.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);

  }

  //dropdown for semester, default is F22
  handleSelect(key){
    let selectedSem = "";
    if(key == 1){
      selectedSem = "F22"
      root4.render(<Images/>);
    }else{
      selectedSem = "W23"
      root4.render(<Images/>);
    }
    selectedSemester = selectedSem;

    this.setState({semester: selectedSem})
    console.log(selectedSem);
  }

  // filtering selected lab days off, default is 'None'
  handleLabDaySelect(key){
    
    console.log("key = ", key.target.id, "Is checked = ", key.target.checked);

    if(key.target.id == 6){
      if(key.target.checked == 1){
        selectedLab.push("Mon")
      }else{
        selectedLab = selectedLab.filter(function(lab){
          return lab != "Mon"
        })
      }
      
    }else if(key.target.id == 7){
      if(key.target.checked == 1){
        selectedLab.push("Tues")
      }else{
        selectedLab = selectedLab.filter(function(lab){
          return lab != "Tues"
        })
      }
    }else if(key.target.id == 8){
      if(key.target.checked == 1){
        selectedLab.push("Wed")
      }else{
        selectedLab = selectedLab.filter(function(lab){
          return lab != "Wed"
        })
      }
    }else if(key.target.id == 9){
      if(key.target.checked == 1){
        selectedLab.push("Thur")
      }else{
        selectedLab = selectedLab.filter(function(lab){
          return lab != "Thur"
        })
      }
    }else if(key.target.id == 10){
      if(key.target.checked == 1){
        selectedLab.push("Fri")
      }else{
        selectedLab = selectedLab.filter(function(lab){
          return lab != "Fri"
        })
      }
    }
    
      
    this.setState({lab: selectedLab})
    //console.log(this.state.lab);
    // console.log("lab" ,selectedLab);
  }
  // filtering selected lecture days off, default is 'None'
  handleDaySelect(key){
    
    console.log("key = ", key.target.id, "Is checked = ", key.target.checked);

    if(key.target.id == 1){
      if(key.target.checked == 1){
        selectedDay.push("Mon")
      }else{
        selectedDay = selectedDay.filter(function(day){
          return day != "Mon"
        })
      }
      
    }else if(key.target.id == 2){
      if(key.target.checked == 1){
        selectedDay.push("Tues")
      }else{
        selectedDay = selectedDay.filter(function(day){
          return day != "Tues"
        })
      }
    }else if(key.target.id == 3){
      if(key.target.checked == 1){
        selectedDay.push("Wed")
      }else{
        selectedDay = selectedDay.filter(function(day){
          return day != "Wed"
        })
      }
    }else if(key.target.id == 4){
      if(key.target.checked == 1){
        selectedDay.push("Thur")
      }else{
        selectedDay = selectedDay.filter(function(day){
          return day != "Thur"
        })
      }
    }else if(key.target.id == 5){
      if(key.target.checked == 1){
        selectedDay.push("Fri")
      }else{
        selectedDay = selectedDay.filter(function(day){
          return day != "Fri"
        })
      }
    }
    
      
    this.setState({day: selectedDay})
    //console.log(this.state.day);
    // console.log("lec" , selectedDay);
  }
  
  //store into searchFor in this.state
  handleChange(event) {
    event.preventDefault();
    this.setState({searchFor: event.target.value});
  }

  //function that's called when 'Search' is clicked, handles GET ajax call to get json formatted data of searched course
  handleSubmit(event){
    event.preventDefault();
    let searchFor = this.state.searchFor;
    let semester = this.state.semester;
    var dayOff = selectedDay;
    let mon = "None"
    let tues = "None"
    let wed = "None"
    let thurs = "None"
    let fri = "None"
    let labMon = "None"
    let labTues = "None"
    let labWed = "None"
    let labThurs = "None"
    let labFri = "None"


    // check if selectedDay array has any filters 
    if(selectedDay.includes("Mon")){
      mon = "Mon"
    }
    if(selectedDay.includes("Tues")){
      tues = "Tues"
    }
    if(selectedDay.includes("Wed")){
      wed = "Wed"
    }
    if(selectedDay.includes("Thur")){
      thurs = "Thur"
    }
    if(selectedDay.includes("Fri")){
      fri = "Fri"
    }
    if(selectedLab.includes("Mon")){
      labMon = "Mon"
    }
    if(selectedLab.includes("Tues")){
      labTues = "Tues"
    }
    if(selectedLab.includes("Wed")){
      labWed = "Wed"
    }
    if(selectedLab.includes("Thur")){
      labThurs = "Thur"
    }
    if(selectedLab.includes("Fri")){
      labFri = "Fri"
    }
    // console.log("LAB array = ", selectedLab)
    
    // console.log("DAY OFF ", dayOff)

    //get rid of tabs, enter, spaces
    searchFor = searchFor.replace(/\s\s+/g, '')
   
    //check if anything was input and send to back end for searching course data if there is input
    if(searchFor == ""){
      // console.log("pls enter course");

      //set classes to string so when printing to the screen can print it in a div like the other outputs
      this.setState({clicked:true, empty:true});
    }else{

      //same formatting as regular js ajax call
      $.ajax({
        type:'GET',
        url: "/getClasses",
        data: {
          searchFor,
          semester,
          mon,
          tues,
          wed,
          thurs,
          fri,
          labMon,
          labTues,
          labWed,
          labThurs,
          labFri
          
        },
        success: function(result){ 

        //put result into the state and use for printing into table format so user can click the add button
        let json = JSON.parse(result);
        

         this.setState({
          table: json, 
          clicked:true, 
          empty:false,
          badcourse:false
        });  
        
        }.bind(this),
        error:function(e){
          console.log(e)
          this.setState({
            empty:false,
            clicked:true,
            badcourse:true
          })
        }.bind(this)
      });

    }
  }


  // adding classes from returned results
  handleAdd(event, selected){
    this.added.current.click();


    let name = selected.name; 
    let tempName = name.split(' ');
    tempName.splice(1,1);
    tempName = tempName.join(' ');

    // console.log("name " + tempName);
    let term = selected.term;
    let capacity = selected.capacity;
    let status = selected.status;
    let faculty = selected.faculty;
    let credit = selected.credit;
    let level = selected.level;
    let location = selected.location;
    let meetings = selected.meetings;


    let alreadyAdded = false;

    // check if the class is already added to the schedule
    if (term == "Fall 2022")  {
      Array.from(jsonClassesF).map((t, index) => {
        if(t.title == tempName){
            alreadyAdded = true;
        }
       
      });
      // show fall calendar
      calendar.render();
      semCal = "F22";
      root3.render(<CalName/>);
    }
    else if (term == "Winter 2023") {
      Array.from(jsonClassesW).map((t, index) => {
        if(t.title == tempName){
          alreadyAdded = true;
        }
        
      });

      // show winter calendar
      winterCalendar.render();
      semCal = "W23";
      root3.render(<CalName/>);
    }
   

    // console.log("already added " + String(alreadyAdded));

    if(alreadyAdded == false){
      addedClass = true;
    
      $.ajax({
        type:'POST',
        url: "/saveSelected",
        data: {name, term, capacity, status, faculty, credit, level, location, meetings},
        success: function(result){ 
          // console.log(result); //for testing
  
          //put result into the state and use for printing into table format 
          const myArray = result.split("|");
  
          // console.log(jsonClasses);
          if (term == "Fall 2022")  {
            jsonClassesF.push(JSON.parse(myArray[0]));
            calendar.addEvent(JSON.parse(myArray[0]));
            calendar.addEvent(JSON.parse(myArray[1]));
          }
          else if (term == "Winter 2023") {
            jsonClassesW.push(JSON.parse(myArray[0]));
            winterCalendar.addEvent(JSON.parse(myArray[0]));
            winterCalendar.addEvent(JSON.parse(myArray[1]));
          }

          addedClass = true;
  
          this.setState({
            clicked:true
          });  
  
        }.bind(this)
      });
    }
   
  }

  //formats table to added courses from the search results
  showSearchResults(){

    // check entered course is in correct formatting 
    if (this.state.clicked && this.state.searchFor.length != 0 && this.state.badcourse == true) {
      return(
        <div className="table-wrapper pt-3">
          <h2>Course not found</h2>
        </div>
      )
    } else if(this.state.clicked && this.state.searchFor.length != 0 && this.state.badcourse == false){
      // returning table with courses if search input passes
      return (
        <div className="table-wrapper pt-3 pd-4" id = "mainText">
          <table className="table text-white table-hover">
            <tbody>
              {/* uses returned json statement from GET call to create table */}

              {Array.from(this.state.table).map((t, index) =>
                <tr key={index}>
                  <td>{t.name}</td>
                  <td>{t.term}</td>
                  <td>{t.meetings}</td>
                  <td>{t.faculty}</td>
                  <td>{t.status}</td>
                  <td>
                    <button ref={this.target} type="button" className="btn btn-success btn-sm" onClick={(event)=> {this.handleAdd(event, t)}}>
                      <i className="bi bi-plus-lg" ></i>
                    </button>
                  </td>
                </tr>
              )}
            </tbody>
          </table>

        </div>
      );
    } else if (this.state.clicked && this.state.empty) {

      // if nothing was entered in the search
      return(
        <div className="table-wrapper pt-3">
          <h2>Please enter a search query</h2>
        </div>
      )
    }
  }


 
  render(){
    let chosenDays = this.state.day;
    let chosenLabDays = this.state.lab;
    
    if(chosenDays.length == 0){
      chosenDays = "None";
    }else{
      chosenDays = chosenDays.join(", ");
    }

    if(chosenLabDays.length == 0){
      chosenLabDays = "None";
    }else{
      chosenLabDays = chosenLabDays.join(", ");
    }

    return(
      <div className="pt-3">
        <div className= "mx-5 px-3 mt-3"> 

          {/* choose semester */}
          <div className="d-flex flex-row pt-3">
            <DropdownButton
              id="semDropDown"
              title="Semester"
              onSelect={this.handleSelect}
              // activekey={this.state.semester}
            >
              <Dropdown.Item eventKey="1">F22</Dropdown.Item>
              <Dropdown.Item eventKey="2">W23</Dropdown.Item>
            </DropdownButton>
            <div className="ps-3 pt-1">
              {this.state.semester}
            </div>
          </div>
          
          {/* choosing specific lecture day(s) to not show up */}
          <div className="d-flex flex-row pt-3">
            <DropdownButton
              
              title="Lecture Day(s) Off"
              id="dayDropDown">
              <form>
                <div className="multiselect px-3">
                  <div className="form-check">
                    <input className="form-check-input" type="checkbox" id="1" onChange={this.handleDaySelect} />
                    <label className="form-check-label" htmlFor="1">
                      Monday
                    </label>
                  </div>
                  <div className="form-check">
                    <input className="form-check-input" type="checkbox" id="2" onChange={this.handleDaySelect}/>
                    <label className="form-check-label" htmlFor="2">
                      Tuesday
                    </label>
                  </div>
                  <div className="form-check">
                    <input className="form-check-input" type="checkbox" id="3" onChange={this.handleDaySelect}/> 
                    <label className="form-check-label" htmlFor="3">
                      Wednesday
                    </label>
                  </div>
                  <div className="form-check">
                    <input className="form-check-input" type="checkbox" id="4" onChange={this.handleDaySelect}/> 
                    <label className="form-check-label" htmlFor="4">
                      Thursday
                    </label>
                  </div>
                  <div className="form-check">
                    <input className="form-check-input" type="checkbox" id="5" onChange={this.handleDaySelect}/> 
                    <label className="form-check-label" htmlFor="5">
                      Friday
                    </label>
                  </div>
                </div>
              </form>
            </DropdownButton>

            {/* show chosen days on the side */}
            <div className="ps-3 pt-1" >
              {chosenDays}
            </div>
          </div>

          {/* choosing specific lab/seminar day(s) to not show up */}
          <div className="d-flex flex-row pt-3">
            <DropdownButton
              
              title="Lab/Seminar Day(s) Off"
              id="labDropDown">
              <form>
                <div className="multiselect px-3">
                  <div className="form-check">
                    <input className="form-check-input" type="checkbox" id="6" onChange={this.handleLabDaySelect} />
                    <label className="form-check-label" htmlFor="6">
                      Monday
                    </label>
                  </div>
                  <div className="form-check">
                    <input className="form-check-input" type="checkbox" id="7" onChange={this.handleLabDaySelect}/>
                    <label className="form-check-label" htmlFor="7">
                      Tuesday
                    </label>
                  </div>
                  <div className="form-check">
                    <input className="form-check-input" type="checkbox" id="8" onChange={this.handleLabDaySelect}/> 
                    <label className="form-check-label" htmlFor="8">
                      Wednesday
                    </label>
                  </div>
                  <div className="form-check">
                    <input className="form-check-input" type="checkbox" id="9" onChange={this.handleLabDaySelect}/> 
                    <label className="form-check-label" htmlFor="9">
                      Thursday
                    </label>
                  </div>
                  <div className="form-check">
                    <input className="form-check-input" type="checkbox" id="10" onChange={this.handleLabDaySelect}/> 
                    <label className="form-check-label" htmlFor="10">
                      Friday
                    </label>
                  </div>
                </div>
              </form>
            </DropdownButton>

            {/* show chosen days on the side */}
            <div className="ps-3 pt-1" >
              {chosenLabDays}
            </div>
          </div>
        </div>

        {/* form for input will always be shown */}
        <form className= "mx-5 px-3 mt-5 pt-4 mb-5" onSubmit={this.handleSubmit} style={{textAlign:"center"}} > 
          <input  type="text" id="courseCode" name="courseCode" value={this.state.searchFor} onChange={this.handleChange} style={{width:"30%", fontSize:"20px"}} className="py-1" placeholder="eg.cis"/> 
          <button ref={this.added} id="searchButton" type="submit" className="ms-3 btn btn-md btn-outline-light" style={{marginBottom:"4px"}}>SEARCH</button>
        </form>

        {/* table for search resutlts and adding classes created */}
        {this.showSearchResults()}
      </div>
    );
  }

}

// title for schedule
class CalName extends React.Component{
  render(){
      if(semCal == "F22"){
        return(
          <div>
            Fall 2022 Schedule
          </div>
        );
      }else{
        return(
          <div>
            Winter 2023 Schedule
          </div>
        );
      }
     
  }
}

// leaves and snowflakes
class Images extends React.Component{
  render(){
    if(selectedSemester == "F22"){
      return(
        <div className="set">
          <div><img src="../static/images/leaf1-cutout.png"width="35"></img></div>
          <div><img src="../static/images/leaf2-cutout.png"width="35"></img></div>
          <div><img src="../static/images/leaf3-cutout.png"width="35"></img></div>
          <div><img src="../static/images/leaf4-cutout.png"width="35"></img></div>
          <div><img src="../static/images/leaf5-cutout.png"width="35"></img></div>
          <div><img src="../static/images/leaf6-cutout.png"width="35"></img></div>
          <div><img src="../static/images/leaf1-cutout.png"width="35"></img></div>
          <div><img src="../static/images/leaf2-cutout.png"width="35"></img></div>
          <div><img src="../static/images/leaf3-cutout.png"width="35"></img></div>
          <div><img src="../static/images/leaf4-cutout.png"width="35"></img></div>
          <div><img src="../static/images/leaf5-cutout.png"width="35"></img></div>
          <div><img src="../static/images/leaf6-cutout.png"width="35"></img></div>
        </div>
      );
  } else {
    return(
      <div className="set">
        <div><img src="../static/images/snowflake.png"width="35"></img></div>
        <div><img src="../static/images/snowflake.png"width="35"></img></div>
        <div><img src="../static/images/snowflake.png"width="35"></img></div>
        <div><img src="../static/images/snowflake.png"width="35"></img></div>
        <div><img src="../static/images/snowflake.png"width="35"></img></div>
        <div><img src="../static/images/snowflake.png"width="35"></img></div>
        <div><img src="../static/images/snowflake.png"width="35"></img></div>
        <div><img src="../static/images/snowflake.png"width="35"></img></div>
        <div><img src="../static/images/snowflake.png"width="35"></img></div>
        <div><img src="../static/images/snowflake.png"width="35"></img></div>
        <div><img src="../static/images/snowflake.png"width="35"></img></div>
        <div><img src="../static/images/snowflake.png"width="35"></img></div>
      </div>

    )
  }
}

}

const calName = document.getElementById('calName');
const root3 = ReactDOM.createRoot(calName);

const search = document.getElementById('search');
const root = ReactDOM.createRoot(search);
root.render(<Search/>);


const images = document.getElementById('images')
const root4 = ReactDOM.createRoot(images);
root4.render(<Images/>);

// full calendar 
var calendarEl = document.getElementById('calendar');
var element = document.getElementById('calendar');

// inializing styling of calendar 
var calendar = new FullCalendar.Calendar(calendarEl, {
  //themeSystem: 'bootstrap5',
  weekends: false,
  initialView: 'timeGridWeek',
  timeZone: 'UTC',
  slotMinTime: "08:30:00",
  slotMaxTime: "23:00:00",
  allDaySlot: false,
  dayHeaderFormat: {
    weekday:'long'
  },
  events: '',
  customButtons: {
    F22Button: {
      text: 'Fall 2022',
      click: function() {
        calendar.render();
        semCal = "F22";
        root3.render(<CalName/>);
      }
    },
    W23Button: {
      text: 'Winter 2023',
      click: function() {
        winterCalendar.render();
        semCal = "W23";
        root3.render(<CalName/>);

      }
    }
  },
  headerToolbar: {
    left: 'F22Button W23Button',
    center: '',
    right: ''
  }
  
});

var winterCalendar = new FullCalendar.Calendar(calendarEl, {
  weekends: false,
  initialView: 'timeGridWeek',
  timeZone: 'UTC',
  slotMinTime: "08:30:00",
  slotMaxTime: "23:00:00",
  allDaySlot: false,
  dayHeaderFormat: {
    weekday:'long'
  },
  events: '',
  //headerToolbar:false
  customButtons: {
    F22Button: {
      text: 'Fall 2022',
      click: function() {
        calendar.render();
        semCal = "F22";
        root3.render(<CalName/>);

      }
    },
    W23Button: {
      text: 'Winter 2023',
      click: function() {
        winterCalendar.render();
        semCal = "W23";
        root3.render(<CalName/>);

      }
    }
  },
  headerToolbar: {
    left: 'F22Button W23Button',
    center: '',
    right: ''
  }
  
});

calendar.render();
semCal = "F22";

