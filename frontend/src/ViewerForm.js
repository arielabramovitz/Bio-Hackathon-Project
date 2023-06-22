import Button from "@mui/material/Button";
import InputAdornment from '@mui/material/InputAdornment';
import {TextField, Typography} from "@mui/material/";
import axios from "axios";

import * as React from 'react';
import {useState} from "react";

export default function ViewerForm({setView, submitForm}) {
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