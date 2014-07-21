////////////////////////// GLOBAL VARIABLES ////////////////////////////////

app.beginUndoGroup("Automation"); 

var RenderSettingsTemp = "Best Settings";
var OutputModuleTemp = "H.264";
var OutputPath = "C:\\Users\\animator\\Desktop\\";
var jobNumber = 1;
var numGroups = 3; // Number of the types of images groups we have. For example, templates that use 1 image, 2 images, or 3 images. THIS IS NOT NUMBER OF TOTAL TEMPLATES!!!!!!!!!
//This is the currently active job number as a string
job = padJob(jobNumber);

var masterFolderPath = "C:\\Users\\animator\\Desktop\\Job" + job + "\\"; //This is the folder where all of the projects are stored

//Create a number padding. This will turn "1" into "0001" 
function padJob(number){
	if (number <= 9999) {
		number = ("000" + number).slice(-4);
		return number;
	}
}

//This is the folder of the current job
var currentFolder = new Folder(masterFolderPath);

var jobCSV = new File(masterFolderPath + "job" + job + ".csv");

//////////////////////////////////////////////////////////////////////////// OPEN THE CSV

//Check to see if the current Job Folder exists. 
//If it does, run the master function. If it doesn't, wait and run the loop again.
if (currentFolder.exists && jobCSV.exists){
	
	//open the jobCSV spreadsheet and read it
	jobCSV.open("r");
	var CSVContents = jobCSV.read();
	var itemsArray = CSVContents.split(/\n|\r/);
	var itemsObject = new Object();

	for (i = 0; i < itemsArray.length; i++){
		itemsArray[i]= itemsArray[i].split(",");
        itemsObject["upload" + i] = {imageName: itemsArray[i][0]};
	}

	randomCompGeneration();

} else {
	alert("The folder or .CSV doesn't exist!");
}

function randomCompGeneration(){

	/////////////////////////////////////////////////////////////////////////////// GENERATE A RANDOM NUMBER OF COMPS

	var numImages = itemsArray.length; //Number of images submitted by the client
	var groupOrder = []; // Array to hold the type of each group
	var total = 0;
	var canAddNumber = false;

	//Loop through the total number of images with an offset. Create a random number/ order of comps
	for (i = 0; i < numImages - numGroups; i++){
		if (total < numImages - numGroups){
			groupOrder.push(Math.floor(Math.random() * numGroups + 1))
			total += groupOrder[i];
		}

		//If the total is between the number of images and its offset, find the remainder between the two
		if (total >= numImages - numGroups && total <= numImages ){
			var remainder = numImages % total;
			var canAddNumber = true;
		}
	}

	//Add the remainder as the final number to groupOrder
	if (canAddNumber){
		groupOrder.push(remainder);
		total += remainder;
		canAddNumber = false;
	}

	var numberOfOnes = 0;
	var numberOfTwos = 0;
	var numberOfThrees = 0;

	for (i = 0; i < groupOrder.length; i++){
		if (groupOrder[i] == 1){
			numberOfOnes++;
		}
		if (groupOrder[i] == 2){
			numberOfTwos++;
		}
		if (groupOrder[i] == 3){
			numberOfThrees++;
		}
	}

	//////////////////////////////////////////////////////////////////////////// MAIN SCRIPT

	imagesAdded = 0;
	folderTarget = app.project.items.addFolder("RemoveFolder");

	for (var h = 0; h < groupOrder.length; h++){
		if (groupOrder[h] == 1){
			var templateRegEx = new RegExp(/_Template01$/);
			assembleNewComp(1, templateRegEx);
		}

		if (groupOrder[h] == 2){
			var templateRegEx = new RegExp(/_Template02$/);
			assembleNewComp(2, templateRegEx);
		}

		if (groupOrder[h] == 3){
			var templateRegEx = new RegExp(/_Template03$/);
			assembleNewComp(3, templateRegEx);
		}
	} // For loop for the main function
	renderFinal();

	for (z = 1; z <= app.project.numItems; z++){
		if (app.project.item(z).name == "RemoveFolder"){
			app.project.item(z).remove();
		}
	}
}


function assembleNewComp(numImages, templateNeeded){
	var foundTemplate = false;
	for (var j = 1; j <= app.project.numItems; j++){
    
        if (app.project.item(j).name.match(templateNeeded)) {
            //alert("Found Template Comp: " + app.project.item(j).name + " it is index: " + j);
            templateComp = app.project.item(j);
            if (templateComp instanceof CompItem){
                
                foundTemplate = true;
                
                } else {
                   alert("Found template, but it is not a comp."); 
            }
        }
	}

	if (foundTemplate){
        var dupeComp = templateComp.duplicate();
        dupeComp.parentFolder = folderTarget;
        dupeComp.name = templateComp.name.replace(templateNeeded, " - " + "Remove");
        for (var c = 1; c <= numImages; c++){
	        var io = new ImportOptions(File(masterFolderPath + itemsArray[imagesAdded][0]));
	        var newImport = app.project.importFile(io);
	        newImport.name = "Remove";
	        newImport.parentFolder = folderTarget;

	        for (d = 1; d <= dupeComp.numLayers; d++){
	        	if (dupeComp.layer(d).name.match("ReplaceMe_" + c)){
	        		dupeComp.layer(d).replaceSource(newImport, false);
	        		if (newImport.width > newImport.height){
	        			var percentScale = 1920 / newImport.width * 100;
	        			var curScale = dupeComp.layer(d).scale.value;
	        			var percentOfCurScale = curScale[1] / 100;
	        			dupeComp.layer(d).scale.setValue([percentScale * percentOfCurScale, percentScale * percentOfCurScale, percentScale * percentOfCurScale]);
	        		}

	        		if (newImport.height > newImport.width || newImport.height == newImport.width){
	        			var percentScale = 1080 / newImport.height * 100;
	        			var curScale = dupeComp.layer(d).scale.value;
	        			var percentOfCurScale = curScale[1] / 100;
	        			dupeComp.layer(d).scale.setValue([percentScale * percentOfCurScale, percentScale * percentOfCurScale, percentScale * percentOfCurScale]);
	        		}
	        	}
	        }

	        imagesAdded++;
        }
        for (e = 1; e <= app.project.numItems; e++){
        	if (app.project.item(e).name == "00_MasterComp"){
        		var masterCompLayer = app.project.item(e);
        	}
	    }

        masterCompLayer.layers.add(dupeComp);
                     
    } else {alert("Could not find the template")}

    for(m = 1; m <= masterCompLayer.numLayers; m++){
    	var offset = m - 1;
    	masterCompLayer.layer(m).startTime = 5 * offset;
    }

} // assembleNewComp

function renderFinal(){

	for (n = 1; n <= app.project.numItems; n++){
    	if (app.project.item(n).name == "00_MasterComp"){
    		var mastComp = app.project.item(n);
    	}
	}

	mastComp.duration = mastComp.numLayers * 5;

	//Add to render queue
    var myRQItem = app.project.renderQueue.items.add(mastComp);
    
    var myRSTemplates = app.project.renderQueue.item(1).templates;
    var foundTemplate = false;
    
    for (var j = 0; j < myRSTemplates.length; j++) {
            if ( myRSTemplates[j] == RenderSettingsTemp){
                    foundTemplate = true;
                    break;
             }
        }
    
    //Apply render settings
    if (foundTemplate){
        
        myRQItem.applyTemplate(RenderSettingsTemp);
        } else {
          alert("Could not find render Setting: " + RenderSettingsTemp);  
        }    
    
        //Apply OM Template
        myRQItem.outputModules[1].applyTemplate(OutputModuleTemp);
        
        var projName = app.project.file.name;
        var myFile = new File(OutputPath + projName.substring(0, projName.length - 4) + "_" + mastComp.name + "_Job" + job);
        
        //Set output path
        myRQItem.outputModules[1].file = myFile;

app.project.renderQueue.render();

}