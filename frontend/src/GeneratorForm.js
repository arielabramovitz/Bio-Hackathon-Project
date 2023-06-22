import Button from "@mui/material/Button";
import InputAdornment from '@mui/material/InputAdornment';
import {TextField, Typography} from "@mui/material/";
import axios from "axios";

import * as React from 'react';
import {useState} from "react";



export default function GeneratorForm({setView, submitForm}) {
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