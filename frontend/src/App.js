import * as React from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Button from "@mui/material/Button";
import './App.css';
import {useState} from "react";
import {CssBaseline, TextField, Typography} from "@mui/material/";
import axios from "axios";
import Card from '@mui/material/Card';
import InputAdornment from '@mui/material/InputAdornment';
import {theme} from "./theme.js"
import {ThemeProvider} from "@mui/material/styles"
import LoadingSpinner from './LoadingSpinner';



function submitForm(form, setView) {
    setView("loading")
    axios.defaults.headers.post['Content-Type'] = 'multipart/form-data';
    axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';
    const cfg = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    axios.post("http://localhost:5000/api", form, cfg)
            .then((res)=>{
                setView(res.data.html)
            })
            .catch((e)=>{console.error(e)})
}

function UpscalerForm({setView}) {

    const [coorFileName, setCoorFileName] = useState("")
    const [coorUploaded, setCoorUploaded] = useState(false)

    function handleUpload(e) {
        setCoorUploaded(e.target?.files[0]?.name!==undefined)
        setCoorFileName(e.target?.files[0]?.name)
        
    }
    

    const handleSubmit = (e)=> {
        e.preventDefault()
        var bodyFormData = new FormData();
        bodyFormData.append('type', 'upscaler')
        bodyFormData.append('coordinateFile', e.target.elements[0].files[0])
        bodyFormData.append('scaleAmount', e.target.scaleAmount.value)
        submitForm(bodyFormData, setView)
    }

    return (
        <form onSubmit={handleSubmit}>
            <div className="UploadButton">
                <Button
                    variant="contained"
                    component="label"
                    >
                    Upload Coordinates
                    <input
                        name='coordinateFile-upscale'
                        type="file"
                        hidden
                        onChange={handleUpload}
                        required
                    />
                </Button>
                {coorUploaded && (
                    <TextField
                    className='FileName'
                    label="File Name"
                    variant="outlined"
                    value={coorFileName}
                    sx={{marginLeft:"10px"}}
                    disabled
                    />
                    )}
            </div>
            <div>
            <TextField
                label="Scale Amount"
                id="scaleAmount"
                sx={{ m: 1, width: '25ch' }}
                InputProps={{
                    startAdornment: <InputAdornment position="start">X</InputAdornment>,
                }}
                required
                />
            </div>
            <div className='SubmitButton'>
                <Button type="submit" variant='contained'>
                    Submit
                </Button>
            </div>
        </form>
    )
}

function GeneratorForm({setView}) {
    const [configFileName, setConfigFileName] = useState("")
    const [configUploaded, setConfigUploaded] = useState(false)

    function handleUpload(e) {

        
        setConfigUploaded(e.target?.files[0]?.name!==undefined)
        setConfigFileName(e.target?.files[0]?.name)
        
    }

    
    
    const handleSubmit = (e)=> {
        e.preventDefault()
        var bodyFormData = new FormData();
        bodyFormData.append('type', 'generator')
        bodyFormData.append('configFile', e.target.elements[0].files[0])
        submitForm(bodyFormData, setView)
    }
    return (
        <form onSubmit={handleSubmit}>
            <div className="UploadButton">
                <Button
                    variant="contained"
                    component="label"
                    >
                    Upload Configuration
                    <input
                    className='FileName'
                        name='configFile-generator'
                        type="file"
                        hidden
                        onChange={handleUpload}
                        required
                    />
                </Button>
                {
                    configUploaded && (
                        <TextField
                        id="outlined-basic"
                        sx={{marginLeft:"10px"}}
                        label="File Name"
                        variant="outlined"
                        value={configFileName}
                        disabled
                        />
                    )
                    }
            </div>
            <div className='SubmitButton'>
                <Button type="submit" variant='contained'>
                    Submit
                </Button>
            </div>
        </form>
    )
}

function ViewerForm({setView}) {
    const [coorFileName, setCoorFileName] = useState("")
    const [coorUploaded, setCoorUploaded] = useState(false)

    function handleUpload(e) {
        
        setCoorUploaded(e.target?.files[0]?.name!==undefined)
        setCoorFileName(e.target?.files[0]?.name)
        
    }

    const handleSubmit = (e)=> {
        e.preventDefault()
        var bodyFormData = new FormData();
        bodyFormData.append('type', 'viewer')
        bodyFormData.append('coordinateFile', e.target.elements[0].files[0])
        submitForm(bodyFormData, setView)
    }

    return (
        <form onSubmit={handleSubmit}>
            
            <div className="UploadButton">
                <Button
                    variant="contained"
                    component="label"
                    >
                    Upload Coordinates
                    <input
                        className='FileName'
                        name='coordinateFile-viewer'
                        type="file"
                        hidden
                        onChange={(e)=>handleUpload(e)}
                        required
                    />
                </Button>
                {coorUploaded && (
                    <TextField
                    className='FileName'
                    sx={{marginLeft:"10px"}}

                    id="outlined-basic"
                    label="File Name"
                    variant="outlined"
                    value={coorFileName}
                    disabled
                    />
                    )}
            </div>
            
            <div className='SubmitButton'>
                <Button type="submit" variant='contained'>
                    Submit
                </Button>
            </div>
        </form>
    )

}

function App() {
    const [view, setView] = useState(null)
    const [formType, setFormType] = useState("upscaler");

    const handleChange = (e) => {

        setFormType(e.target.value)
        setView(null)
    }

    const switchView = ()=>{
        switch(view){
            case null: return null;
            case "loading": return <LoadingSpinner/>;
            default: return <iframe title='visualizer-iframe' className="Graph" srcDoc={view}></iframe>
        }
    }
    
    const renderForm = (setView)=>{
        
            switch (formType) {
                case 'upscaler':
                    return <UpscalerForm setView={setView}/>;
                case 'generator':
                    return <GeneratorForm setView={setView}/>;
                case 'viewer':
                    return <ViewerForm setView={setView}/>;
                default:
                    return <UpscalerForm setView={setView}/>;
            }
    }

    return (

        <ThemeProvider theme={theme}>
            <CssBaseline enableColorScheme/>
            <div className="App">
            <Card className="Card">

                <div className="Title">
                    <Typography variant="h3">
                        Virtual Telescope
                    </Typography>
                    <Typography variant="h6">
                        A molecular dynamics Upscaler/Visualizer
                    </Typography>
                </div>
                    <Card>
                        <div className="FormControl">
                            <FormControl name="Form" variant="filled" fullWidth={true}>
                                <InputLabel id="demo-simple-select-label">Form Type</InputLabel>
                                <Select
                                    value={formType}
                                    onChange={handleChange}
                                >
                                    <MenuItem value={"upscaler"}>Upscaler</MenuItem>
                                    <MenuItem value={"generator"}>Generator</MenuItem>
                                    <MenuItem value={"viewer"}>Viewer</MenuItem>
                                </Select>
                            </FormControl>
                        
                        </div>
                    {renderForm(setView)}
                    </Card>
                    {switchView()}
                    
                    
                </Card>
            </div>

        </ThemeProvider>
    );
}

export default App;
