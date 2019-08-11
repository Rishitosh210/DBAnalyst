import React from 'react';
import {BrowserRouter as Router, Route} from "react-router-dom";
import {Button, Layout, Menu, message} from 'antd';
import RegistrationModal from './RegisterModal'
import DataUpload from './DataUpload'
import LoginModal from './LoginModal'
import axios from "axios";

const {Content, Footer} = Layout;

export default class LayoutDetail extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            show: false
        }
    }

    logout() {
        axios.post(`http://127.0.0.1:8000/logout/`).then((res) => {
            message.success(`Logout Successfully`)
        })
    }

    render() {
        return (
            <>

                <div className="logo"/>
                <Menu
                    theme="light"
                    mode="horizontal"
                    style={{lineHeight: '64px'}}
                >
                    <Menu.Item key="1"><RegistrationModal/></Menu.Item>
                    <Menu.Item key="2"><LoginModal/></Menu.Item>
                    <Menu.Item key="3">
                        <Button type="primary" key="4" onClick={this.logout}>
                            Logout
                        </Button>
                    </Menu.Item>
                </Menu>

                <Layout className="layout">
                    <Content style={{padding: '0 50px', marginTop: 15}}>
                        <Router>
                            <div style={{background: '#fff', minHeight: 600}}>
                                <Route exact path='/' component={DataUpload}/>
                            </div>
                        </Router>
                    </Content>
                    <Footer style={{textAlign: 'center', fontSize: '10px'}}>
                        CA Hand Design ©2018 Created by Rishitosh
                        Guha
                    </Footer>
                </Layout>
            </>
        );
    }
}

