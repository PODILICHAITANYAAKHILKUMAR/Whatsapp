import React, { useState } from "react"; 
import axios from 'axios';
import {SEND_MESSAGES_API} from './constants' 
function FileUploader() 
{ 
    const [selectedFile, setSelectedFile] = useState(null);

const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
}

const handleSendMessages = async () => {
    if (!selectedFile) return alert("Please select a file first.");
    const formData = new FormData();
    formData.append("file", selectedFile);
    try {
        const response = await axios.post(SEND_MESSAGES_API, formData);
        const data = await response.json();
        alert(data.message);
    } catch (error) {
        alert("Failed to send messages.");
    }
};

return (
    <div>
        <h2>Select CSV/XLSX File</h2>
        <input type="file" accept=".csv, .xlsx" onChange={handleFileChange} />
        <button onClick={handleSendMessages}>Send Messages</button>
    </div>
);
}

export default FileUploader;