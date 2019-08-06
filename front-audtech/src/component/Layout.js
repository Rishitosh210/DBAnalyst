import React from 'react';
import {Layout, Menu} from 'antd';
import RegistrationModal from './RegisterModal'
import  DataUpload from  './DataUpload'

const {Header, Content, Footer} = Layout;

export default class LayoutDetail extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            show: false
        }
    }

    render() {
        return (
            <>
                <Header style={{background:'#005fff'}}>
                    <Menu
                        theme="light"
                        mode="horizontal"
                        style={{lineHeight: '64px'}}
                    >
                        <Menu.Item key="1"> <RegistrationModal/></Menu.Item>
                        <Menu.Item key="2">Create User </Menu.Item>
                        <Menu.Item key="3">Create Something</Menu.Item>
                    </Menu>
                </Header>
                <Layout className="layout">
                    <Content style={{padding: '0 50px', margin: '16px 0'}}>
                        <div style={{background: '#fff', minHeight: 600}}>
                            <DataUpload/>
                        </div>
                    </Content>
                    <Footer style={{textAlign: 'center', fontSize: '10px'}}>CA Hand Design ©2018 Created by Rishitosh
                        Guha</Footer>
                </Layout>
            </>
        );
    }
}

