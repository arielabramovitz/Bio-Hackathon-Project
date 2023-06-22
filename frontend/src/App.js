import * as React from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, {SelectChangeEvent} from '@mui/material/Select';
import Button from "@mui/material/Button";
import './App.css';
import {useState} from "react";
import {TextField, Typography} from "@mui/material/";
import axios from "axios";
import Card from '@mui/material/Card';
import InputAdornment from '@mui/material/InputAdornment';



function submitForm(form, setView) {
    axios.defaults.headers.post['Content-Type'] = 'multipart/form-data';
    axios.defaults.headers.post['Accept'] = 'application/json'
    const cfg = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    axios.post("http://localhost:5000/api", form, cfg)
            .then((res)=>{
                setView(res.body.html)
            })
            .catch((e)=>{console.error(e)})
}

function UpscalerForm({setView}) {

    const [coorFileName, setCoorFileName] = useState("")
    const [coorUploaded, setCoorUploaded] = useState(false)

    function handleUpload(e) {
        setCoorUploaded(true)
        setCoorFileName(e.target.files[0].name)
        
    }

    const handleSubmit = (e)=> {
        e.preventDefault()
        var bodyFormData = new FormData();
        bodyFormData.append('type', 'upscaler')
        bodyFormData.append('coordinateFile', e.target.elements[0].files[0])
        bodyFormData.append('scaleAmount', e.target.scaleAmount.value)
        console.log(bodyFormData)
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
                        type="file"
                        hidden
                        onChange={handleUpload}
                    />
                </Button>
                {coorUploaded && (
                    <TextField
                    id="outlined-basic"
                    label="File Name"
                    variant="outlined"
                    value={coorFileName}
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

        
        setConfigUploaded(true)
        setConfigFileName(e.target.files[0].name)
        
    }

    
    
    const handleSubmit = (e)=> {
        e.preventDefault()
        var bodyFormData = new FormData();
        bodyFormData.append('type', 'upscaler')
        bodyFormData.append('coordinateFile', e.target.elements[0].files[0])
        bodyFormData.append('scaleAmount', e.target.scaleAmount.value)
        console.log(bodyFormData)
        axios.post("localhost:3000/", bodyFormData)
            .then((res)=>{
                setView(res.body.html)
            })
            .catch((e)=>{console.error(e)})
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
                        type="file"
                        hidden
                        onChange={handleUpload}
                    />
                </Button>
                {
                    configUploaded && (
                        <TextField
                        id="outlined-basic"
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
        
        setCoorUploaded(true)
        setCoorFileName(e.target.files[0].name)
        
    }

    const handleSubmit = (e)=> {
        e.preventDefault()
        var bodyFormData = new FormData();
        bodyFormData.append('type', 'upscaler')
        bodyFormData.append('coordinateFile', e.target.elements[0].files[0])
        bodyFormData.append('scaleAmount', e.target.scaleAmount.value)
        console.log(bodyFormData)
        axios.post("localhost:3000/", bodyFormData)
            .then((res)=>{
                setView(res.body.html)
            })
            .catch((e)=>{console.error(e)})
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
                        type="file"
                        hidden
                        onChange={(e)=>handleUpload(e)}
                    />
                </Button>
                {coorUploaded && (
                    <TextField
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
    const [view, setView] = useState()
    const [formType, setFormType] = useState("upscaler");

    const handleChange = (e) => {

        setFormType(e.target.value)
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
                        <FormControl variant="filled" fullWidth={true}>
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
                {view && (
                    <div dangerouslySetInnerHTML={{ __html: view }}>

                    </div>
                )}
            </Card>
        </div>
    );
}

export default App;
