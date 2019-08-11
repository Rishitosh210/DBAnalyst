import React from 'react'
import {Button, Drawer, Form, Icon, Input, message, Tooltip,} from 'antd';
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

class RegistrationModal extends React.Component {
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
                axios.post(`http://127.0.0.1:8000/api/user/list/`, values, {'Content-Type': 'application/json'})
                    .then((res) => {
                        //on success
                        this.setState({
                           visible:false
                        });
                        message.success("Register has been completed " +
                            "successfully "+values.username)
                    })
                    .catch((error) => {
                        console.log(error.response)
                        //on error
                    });
            } else {
                console.log(err, "bhosdhika")
            }
        });

    };

    handleConfirmBlur = e => {
        const {value} = e.target;
        this.setState({confirmDirty: this.state.confirmDirty || !!value});
    };

    showToggle = () => {
        this.setState({
            visible: !this.state.visible,
        });
    };
    compareToFirstPassword = (rule, value, callback) => {
        const {form} = this.props;
        if (value && value !== form.getFieldValue('password')) {
            callback('Two passwords that you enter is inconsistent!');
        } else {
            callback();
        }
    };

    validateToNextPassword = (rule, value, callback) => {
        const {form} = this.props;
        console.log(callback(), "callback")
        if (value && this.state.confirmDirty) {
            form.validateFields(['confirm'], {force: true});
        }
        callback();
    };

    render() {
        const {visible} = this.state;
        const {getFieldDecorator} = this.props.form;

        return (
            <>
                <Button type="primary" onClick={this.showToggle}>
                    Register Yourself
                </Button>
                <Drawer
                    title="Register YourSelf"
                    placement="right"
                    closable={true}
                    width={420}
                    onClose={this.showToggle}
                    visible={visible}
                >
                    <Form {...formItemLayout} hideRequiredMark={true}>
                        <Form.Item label="E-mail">
                            {getFieldDecorator('username', {
                                rules: [
                                    {
                                        type: 'email',
                                        message: 'The input is not valid E-mail!',
                                    },
                                    {
                                        required: true,
                                        message: 'Please input your E-mail!',
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
                                    },
                                    {
                                        validator: this.validateToNextPassword,
                                    },
                                ],
                            })(<Input.Password/>)}
                        </Form.Item>
                        <Form.Item label="Confirm Password" hasFeedback>
                            {getFieldDecorator('confirm', {
                                rules: [
                                    {
                                        required: true,
                                        message: 'Please confirm your password!',
                                    },
                                    {
                                        validator: this.compareToFirstPassword,
                                    },
                                ],
                            })(<Input.Password onBlur={this.handleConfirmBlur}/>)}
                        </Form.Item>
                        <Form.Item
                            label={
                                <span>Nickname&nbsp;
                                    <Tooltip title="What do you want others to call you?">
                                    <Icon type="question-circle-o"/>
                                    </Tooltip>
                                </span>}
                        >
                            {getFieldDecorator('nickname', {
                                rules: [{required: true, message: 'Please input your nickname!', whitespace: true}],
                            })(<Input/>)}
                        </Form.Item>
                        <Form.Item>
                            <Button key="submit" htmlType="submit" type="primary" onClick={this.handleSubmit}>
                                Submit
                            </Button>
                        </Form.Item>
                    </Form>
                </Drawer>
            </>
        );
    }
}

const Register = Form.create({name: 'register'})(RegistrationModal);
export default Register;