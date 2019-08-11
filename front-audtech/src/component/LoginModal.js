import React from 'react'
import {Button, Form, Input, message, Modal,} from 'antd';
import axios from "axios";

const formItemLayout = {
    labelCol: {
        xs: {span: 24},
        sm: {span: 8},
    },
    wrapperCol: {
        xs: {span: 24},
        sm: {span: 16},
    },
};
class LoginModal extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            confirmDirty: false,
            visible: false,
        };
    }

    handleSubmit = e => {
        e.preventDefault();
        this.props.form.validateFieldsAndScroll((err, values) => {
            if (!err) {
                axios.post(`http://127.0.0.1:8000/login/`, values, {'Content-Type': 'application/json'})
                    .then((res) => {
                        this.setState({
                            visible: false
                        });
                        message.success(`Login Successful`)
                    }).catch((error) => {
                    console.log(error.response, "error")
                    //on error
                });
            } else {
                message.error(`Login Unsuccessful`, 1000)
            }
        });

    };

    showToggle = () => {
        this.setState({
            visible: !this.state.visible,
        });
    };

    render() {
        const {visible} = this.state;
        const {getFieldDecorator} = this.props.form;

        return (
            <>
                <Button type="primary" onClick={this.showToggle}>
                    Login Yourself
                </Button>
                <Modal
                    visible={visible}
                    title="Login Please "
                    onCancel={this.showToggle}
                    footer={[
                        <Button className="btn btn-primary" key="back" onClick={this.handleSubmit}>
                            Return
                        </Button>
                    ]}
                >
                    <Form {...formItemLayout} hideRequiredMark={true}>
                        <Form.Item label="UserName">
                            {getFieldDecorator('username', {
                                rules: [
                                    {
                                        message: 'The input is not valid Username!',
                                    },
                                    {
                                        required: true,
                                        message: 'Please input your User Name!',
                                    },
                                ],
                            })(<Input/>)}
                        </Form.Item>
                        <Form.Item label="Password" hasFeedback>
                            {getFieldDecorator('password', {
                                rules: [
                                    {
                                        required: true,
                                        message: 'Please input your password!',
                                    }
                                ],
                            })(<Input.Password/>)}
                        </Form.Item>
                    </Form>
                </Modal>
            </>
        );
    }
}

const Login = Form.create({name: 'login'})(LoginModal);
export default Login;