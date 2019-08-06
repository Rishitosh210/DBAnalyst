import {Button, Icon, message, Upload} from 'antd';
import React from 'react'
import axios from 'axios'


export default class DataUpload extends React.Component {
    constructor(props) {
        super(props);
        this.varibale = {
            name: 'file',
            action: `http://127.0.0.1:8000/upload-data/`,
            headers: {
                'X-CSRF-Token': 'csrftoken'
            }
        };
        this.state = {};
    }

    onChange(info) {
        if (info.file.status !== 'uploading') {
            // console.log(info.file, info.fileList);
        }
        if (info.file.status === 'done') {
            message.success(`${info.file.name} file uploaded successfully`);
        }
            else if (info.file.status === 'error') {
            message.error(`${info.file.name} file upload failed.`);
        }
    }

    beforeUpload = (file) => {
        const reader = new FileReader();
        reader.onload = e => {
            axios.post(`http://127.0.0.1:8000/upload-data/`, reader.result)
                .then(res => {console.log(res,"response")})
                .catch(error =>{
                    console.log("err",error.response)
                })
        };
        reader.readAsText(file);
       return false
    };

    render() {
        return (
            <Upload {...this.varibale} onChange={this.onChange} beforeUpload={this.beforeUpload}>
                <Button>
                    <Icon type="upload"/> Click to Upload
                </Button>
            </Upload>
        )
    }
}
