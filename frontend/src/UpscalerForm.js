import Button from "@mui/material/Button";
import InputAdornment from '@mui/material/InputAdornment';
import {TextField} from "@mui/material/";
import axios from "axios";

import * as React from 'react';
import {useState} from "react";

export default function UpscalerForm({setView, submitForm}) {

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