import React from 'react'
import {Button, Form, Icon, Input, Modal, Tooltip,} from 'antd';
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
const tailFormItemLayout = {
    wrapperCol: {
        xs: {
            span: 24,
            offset: 0,
        },
        sm: {
            span: 16,
            offset: 8,
        },
    },
};

class RegistrationModal extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            confirmDirty: false,
            loading: false,
            visible: false,
        };
    }

    handleSubmit = e => {
        e.preventDefault();
        this.props.form.validateFieldsAndScroll((err, values) => {
            if (!err) {
                axios.post(`http://127.0.0.1:8000/register/`, values, {'Content-Type': 'application/json'}).then((res) => {
                    //on success
                    console.log('Received values of form: ', values);
                    console.log("done", res)
                }).catch((error) => {
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

    showModal = () => {
        this.setState({
            visible: true,
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

    handleOk = () => {
        this.setState({loading: true});
        setTimeout(() => {
            this.setState({loading: false});
        }, 3000);
    };

    handleCancel = () => {
        this.setState({visible: false});
    };

    render() {
        const {visible, loading} = this.state;
        const {getFieldDecorator} = this.props.form;

        return (
            <>
                <Button type="primary" onClick={this.showModal}>
                    Register Yourself
                </Button>
                <Modal
                    visible={visible}
                    title="Register Please "
                    onOk={this.handleOk}
                    onCancel={this.handleCancel}
                    footer={[
                        <Button key="back" onClick={this.handleCancel}>
                            Return
                        </Button>
                    ]}
                >
                    <Form {...formItemLayout} hideRequiredMark={true} onSubmit={this.handleSubmit}>
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
                        <Form.Item {...tailFormItemLayout}>
                            <Button key="submit" htmlType="submit" type="primary" loading={loading}>
                                Submit
                            </Button>
                        </Form.Item>
                    </Form>
                </Modal>
            </>
        );
    }
}

const Register = Form.create({name: 'register'})(RegistrationModal);
export default Register;