import os


def viewer(movie_txt_path):
    # variables
    html_file_name = "viewer.html"
    colors_dict = {"1": "'#70a15d'", "2": "'#70a8b5'", "3": "'#b179c9'"}

    maxXRange = 0.0
    maxYRange = 0.0
    minXRange = 0.0
    minYRange = 0.0
    #

    f = open(html_file_name, "w+")
    HTMLBefore = """<!DOCTYPE html>
    <html>
    <title>XYZ Viewer</title>
    <style>
    .Bar-container{
    margin:0;
    width: 200px;
    height: 10px;
    display:inline-block;}
    .slider {
    width: 100%;
    -webkit-appearance: none;
    background: #aaa;
    outline: none;
    opacity: 0.7;
    -webkit-transition: .2s;
    transition: opacity .2s;
    cursor: pointer;
    }
    .slider:hover {
    opacity: 1;
    }
    .slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 10px;
    height: 10px;
    border-radius:10px;
    background: #111;
    cursor: pointer;
    }
    .slider::-moz-range-thumb {
    width: 10px;
    height: 10px;
    border-radius:10px;
    background: #333;
    cursor: pointer;
    }
    #Frame{width:100px;margin-left:5px;text-align:center}
    #Speed{width:100px;margin-left:5px;margin-right:20px;text-align:center}
    #Size{width:45px;margin-left:5px;text-align:center}
    span{font-size:14px}
    </style>
    <body>
    <div id="myDiv" style='width:95%;margin:auto'></div>
    <div align=center>
       <button id="PlayBtn">Play</button>
       <div class="Bar-container"><input type="range" id="Frame-bar" class="slider" value=0 /></div>
       <input type="text" id="Frame" placeholder="Frame" /><br />
       <span>FPS:<input type="text" id="Speed" value=20 /> 
       Particle Size:<input type="text" id="Size" value=3 /><br /></span><br />
    </div>
    """

    JScript = "<script src='https://cdn.plot.ly/plotly-latest.min.js'></script>\n"

    HTMLAfter = """
    var numberOfFrame = Data.length;
    var FrameBar = document.getElementById('Frame-bar');
    FrameBar.max=numberOfFrame-1;
    var Atom = Data[0].length;
    var x=[];
    var y=[];
    var color=[];
    var names=[];
    var Size = document.getElementById('Size');

    for(var i=0;i<Atom;i++){
        x.push(Data[0][i].coord[0]);
        y.push(Data[0][i].coord[1]);
        color.push(Data[0][i].color);
        names.push(Data[0][i].name);
    }

    Plotly.plot('myDiv',[{
      x: x,
      y: y,
      text: names,
      mode: 'markers',
      type: 'scatter2d',
      marker: {
        color: color,
        size: Size.value,
         line:{color: 'rgb(231, 99, 250)',
          width: 1}
       },
      }],{height:500,
       dragmode: false,   scene:{
        aspectmode: "manual",
       aspectratio: {
         x: 1, y: 1,
        },
       xaxis: {
        range: [minXRange*1.05, maxXRange*1.05],
      },
       yaxis: {
        range: [minYRange*1.05, maxYRange*1.05],
      }},
      });

    var PlayBtn = document.getElementById('PlayBtn');
    var Speed = document.getElementById('Speed');
    var Frame = document.getElementById('Frame');
    
    function Play(U){
        if(PlayBtn.innerHTML!="Stop"){
            if(Speed.value=="")
              { Speed.value=20; }
            if(Frame.value=="")
              { Frame.value=0; }
           if(PlayBtn.innerHTML=="Replay")          
           { Frame.value=0; FrameBar.value=0; }
            Playing = setInterval(function(){
                if((Frame.value>=numberOfFrame-1 || FrameBar.value>=numberOfFrame-1) && PlayBtn.innerHTML!='Play'){
                    PlayBtn.innerHTML="Replay";
                   Frame.value=numberOfFrame-1;
                   FrameBar.value=numberOfFrame-1;
                    window.clearInterval(Playing);
                    return;
                }
                Update(U);
            }, 1000.0/Speed.value);
            PlayBtn.innerHTML="Stop";
        }
        else{
            PlayBtn.innerHTML="Play";
            window.clearInterval(Playing);
        }
    }

    function Update(U){
       var n = parseInt(U.value);
        x=[];
        y=[];
        color=[];
        names=[];
        for(var i=0;i<Atom;i++){
            x.push(Data[n][i].coord[0]);
            y.push(Data[n][i].coord[1]);
            color.push(Data[n][i].color);
            names.push(Data[n][i].name);
        }
        
        Plotly.update('myDiv', {
        x: [x],
        y: [y],
        text: names,
        marker: {
           color: color,
           size: Size.value,
            line:{color: 'rgb(231, 99, 250)',
               width: 1}
           },
        });
       Frame.value=n+1;
       FrameBar.value=n+1;
    }
    
    
    Frame.addEventListener('change', function () {
        if(Playing) window.clearInterval(Playing);
        PlayBtn.innerHTML="Play";
       Update(Frame);
        Frame.value-=1;
    });
    FrameBar.addEventListener('change', function () {
          Play(FrameBar);
       Update(FrameBar);
          Play(FrameBar);
        FrameBar.value-=1;
        Frame.value-=1;
    });
    Frame.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
          Play(Frame);
        }
    });
    Speed.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
          Play(FrameBar);
          Play(FrameBar);
        }
    });
    Size.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
          Update(Frame);
        }
    });
    PlayBtn.onclick = function(){Play(FrameBar)};document.onkeydown = function (e) {
        if (e.key === 'Escape') {
           event.preventDefault(); 	    
           if(Playing) window.clearInterval(Playing);
            PlayBtn.innerHTML="Play";
        }
    };
    </script>
    </body>
    </html>
    """

    data_prefix = "<script>var Data = [\n"

    f.write(HTMLBefore + "\n")
    f.write(JScript + "\n")
    f.write(data_prefix)

    xyz_file = open(movie_txt_path, 'r')
    number_of_frames = int(xyz_file.readline())
    frame_info = xyz_file.readline().split()
    frame_width = int(float(frame_info[0]))
    frame_length = int(float(frame_info[1]))
    number_of_molecules = int(xyz_file.readline())

    # parse data from input file into an array called Data in html:
    for frame in range(number_of_frames):
        xyz_file.readline()  # number of frame
        f.write("  [\n")
        for molecule in range(number_of_molecules):
            current_molecule = xyz_file.readline().split()
            molecule_type = current_molecule[0]
            x_coordinate = current_molecule[1]
            y_coordinate = current_molecule[2]
            color = colors_dict[molecule_type]
            f.write("{name: " + molecule_type + ", ")
            f.write("color : " + color + ", ")
            f.write("coord : [" + x_coordinate + ", " + y_coordinate + ", " + "]}, \n")

            # change boundries based on the movement:
            x_coordinate = float(x_coordinate)
            y_coordinate = float(y_coordinate)
            if x_coordinate > maxXRange:
                maxXRange = x_coordinate
            if x_coordinate < minXRange:
                minXRange = x_coordinate
            if y_coordinate > maxYRange:
                maxYRange = y_coordinate
            if y_coordinate < minYRange:
                minYRange = y_coordinate

        f.write("  ],\n")

    maxRange = max(maxXRange - minXRange, maxYRange - minYRange)
    centreX = 0.5 * (maxXRange + minXRange)
    centreY = 0.5 * (maxYRange + minYRange)
    maxXRange = 0.5 * maxRange + centreX
    minXRange = -0.5 * maxRange + centreX
    maxYRange = 0.5 * maxRange + centreY
    minYRange = -0.5 * maxRange + centreY

    data_suffix = "];\nvar maxXRange=" + str(frame_width) + ", maxYRange=" + str(frame_length) + ",\n   minXRange=" + \
                  str(0) + ",\n    minYRange=" + str(0) + ";\n"

    f.write(data_suffix)
    f.write(HTMLAfter)

    xyz_file.close()


def viewer_3d(movie_txt_path):
    # variables
    html_file_name = "viewer.html"
    colors_dict = {"1": "'#70a15d'", "2": "'#70a8b5'", "3": "'#b179c9'"}

    maxXRange = 0.0
    maxYRange = 0.0
    minXRange = 0.0
    minYRange = 0.0

    maxZRange = 0.0
    minZRange = 0.0
    #

    f = open(html_file_name, "w+")
    HTMLBefore = """<!DOCTYPE html>
    <html>
    <title>XYZ Viewer</title>
    <style>
    .Bar-container{
    margin:0;
    width: 200px;
    height: 10px;
    display:inline-block;}
    .slider {
    width: 100%;
    -webkit-appearance: none;
    background: #aaa;
    outline: none;
    opacity: 0.7;
    -webkit-transition: .2s;
    transition: opacity .2s;
    cursor: pointer;
    }
    .slider:hover {
    opacity: 1;
    }
    .slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 10px;
    height: 10px;
    border-radius:10px;
    background: #111;
    cursor: pointer;
    }
    .slider::-moz-range-thumb {
    width: 10px;
    height: 10px;
    border-radius:10px;
    background: #333;
    cursor: pointer;
    }
    #Frame{width:100px;margin-left:5px;text-align:center}
    #Speed{width:100px;margin-left:5px;margin-right:20px;text-align:center}
    #Size{width:45px;margin-left:5px;text-align:center}
    span{font-size:14px}
    </style>
    <body>
    <div id="myDiv" style='width:95%;margin:auto'></div>
    <div align=center>
       <button id="PlayBtn">Play</button>
       <div class="Bar-container"><input type="range" id="Frame-bar" class="slider" value=0 /></div>
       <input type="text" id="Frame" placeholder="Frame" /><br />
       <span>FPS:<input type="text" id="Speed" value=20 /> 
       Particle Size:<input type="text" id="Size" value=3 /><br /></span><br />
    </div>
    """

    JScript = "<script src='https://cdn.plot.ly/plotly-latest.min.js'></script>\n"

    HTMLAfter = """
    var numberOfFrame = Data.length;
    var FrameBar = document.getElementById('Frame-bar');
    FrameBar.max=numberOfFrame-1;
    var Atom = Data[0].length;
    var x=[];
    var y=[];
    var z=[];
    var color=[];
    var names=[];
    var Size = document.getElementById('Size');

    for(var i=0;i<Atom;i++){
        x.push(Data[0][i].coord[0]);
        y.push(Data[0][i].coord[1]);
        z.push(Data[0][i].coord[2]);
        color.push(Data[0][i].color);
        names.push(Data[0][i].name);
    }

    Plotly.plot('myDiv',[{
      x: x,
      y: y,
      z: z,
      text: names,
      mode: 'markers',
      type: 'scatter3d',
      marker: {
        color: color,
        size: Size.value,
         line:{color: 'rgb(231, 99, 250)',
          width: 1}
       },
      }],{height:500,
       dragmode: "orbit",   scene:{
        aspectmode: "manual",
       aspectratio: {
         x: 1, y: 1, z: 1,
        },
       xaxis: {
        range: [minXRange*1.05, maxXRange*1.05],
      },
       yaxis: {
        range: [minYRange*1.05, maxYRange*1.05],
      },
        zaxis: {
         range: [minXRange*1.05, maxZRange*1.05],
         }},
      })

    var PlayBtn = document.getElementById('PlayBtn');
    var Speed = document.getElementById('Speed');
    var Frame = document.getElementById('Frame');

    function Play(U){
        if(PlayBtn.innerHTML!="Stop"){
            if(Speed.value=="")
              { Speed.value=20; }
            if(Frame.value=="")
              { Frame.value=0; }
           if(PlayBtn.innerHTML=="Replay")          
           { Frame.value=0; FrameBar.value=0; }
            Playing = setInterval(function(){
                if((Frame.value>=numberOfFrame-1 || FrameBar.value>=numberOfFrame-1) && PlayBtn.innerHTML!='Play'){
                    PlayBtn.innerHTML="Replay";
                   Frame.value=numberOfFrame-1;
                   FrameBar.value=numberOfFrame-1;
                    window.clearInterval(Playing);
                    return;
                }
                Update(U);
            }, 1000.0/Speed.value);
            PlayBtn.innerHTML="Stop";
        }
        else{
            PlayBtn.innerHTML="Play";
            window.clearInterval(Playing);
        }
    }

    function Update(U){
       var n = parseInt(U.value);
        x=[];
        y=[];
        z=[];
        color=[];
        names=[];
        for(var i=0;i<Atom;i++){
            x.push(Data[n][i].coord[0]);
            y.push(Data[n][i].coord[1]);
            z.push(Data[n][i].coord[2]);
            color.push(Data[n][i].color);
            names.push(Data[n][i].name);
        }
        Plotly.restyle('myDiv', {
        x: [x],
        y: [y],
        z: [z],
        text: names,
        marker: {
           color: color,
           size: Size.value,
            line:{color: 'rgb(231, 99, 250)',
               width: 1}
           },
        });
       Frame.value=n+1;
       FrameBar.value=n+1;
    }

    Frame.addEventListener('change', function () {
        if(Playing) window.clearInterval(Playing);
        PlayBtn.innerHTML="Play";
       Update(Frame);
        Frame.value-=1;
    });
    FrameBar.addEventListener('change', function () {
          Play(FrameBar);
       Update(FrameBar);
          Play(FrameBar);
        FrameBar.value-=1;
        Frame.value-=1;
    });
    Frame.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
          Play(Frame);
        }
    });
    Speed.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
          Play(FrameBar);
          Play(FrameBar);
        }
    });
    Size.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
          Update(Frame);
        }
    });
    PlayBtn.onclick = function(){Play(FrameBar)};document.onkeydown = function (e) {
        if (e.key === 'Escape') {
           event.preventDefault(); 	    
           if(Playing) window.clearInterval(Playing);
            PlayBtn.innerHTML="Play";
        }
    };
    </script>
    </body>
    </html>
    """

    data_prefix = "<script>var Data = [\n"

    f.write(HTMLBefore + "\n")
    f.write(JScript + "\n")
    f.write(data_prefix)

    xyz_file = open(movie_txt_path, 'r')
    number_of_frames = int(xyz_file.readline())
    frame_info = xyz_file.readline().split()
    frame_width = int(float(frame_info[0]))
    frame_length = int(float(frame_info[1]))
    number_of_molecules = int(xyz_file.readline())

    # parse data from input file into an array called Data in html:
    for frame in range(number_of_frames):
        xyz_file.readline()  # number of frame
        f.write("  [\n")
        for molecule in range(number_of_molecules):
            current_molecule = xyz_file.readline().split()
            molecule_type = current_molecule[0]
            x_coordinate = current_molecule[1]
            y_coordinate = current_molecule[2]
            z_coordinate = "0"
            color = colors_dict[molecule_type]
            f.write("{name: " + molecule_type + ", ")
            f.write("color : " + color + ", ")
            f.write("coord : [" + x_coordinate + ", " + y_coordinate + ", " + z_coordinate + "]}, \n")

            # change boundries based on the movement:
            x_coordinate = float(x_coordinate)
            y_coordinate = float(y_coordinate)
            z_coordinate = float(z_coordinate)
            if x_coordinate > maxXRange:
                maxXRange = x_coordinate
            if x_coordinate < minXRange:
                minXRange = x_coordinate
            if y_coordinate > maxYRange:
                maxYRange = y_coordinate
            if y_coordinate < minYRange:
                minYRange = y_coordinate
            if z_coordinate > maxZRange:
                maxZRange = z_coordinate
            if z_coordinate < minZRange:
                minZRange = z_coordinate

        f.write("  ],\n")

    maxRange = max(max(maxXRange - minXRange, maxYRange - minYRange), maxZRange - minZRange)
    centreX = 0.5 * (maxXRange + minXRange)
    centreY = 0.5 * (maxYRange + minYRange)
    centreZ = 0.5 * (maxZRange + minZRange)
    maxXRange = 0.5 * maxRange + centreX
    minXRange = -0.5 * maxRange + centreX
    maxYRange = 0.5 * maxRange + centreY
    minYRange = -0.5 * maxRange + centreY
    maxZRange = 0.0
    minZRange = 0.0

    data_suffix = "];\nvar maxXRange=" + str(maxXRange) + ", maxYRange=" + str(maxYRange) + ",\n   maxZRange=" + \
                  str(maxZRange) + ", minXRange=" + \
                  str(minXRange) + ",\n    minYRange=" + str(minYRange) + ", minZRange=" + str(minZRange) + ";\n"

    f.write(data_suffix)
    f.write(HTMLAfter)

    xyz_file.close()


if __name__ == '__main__':
    viewer_3d('test_res_upscaled')
