import React from 'react';
import { toast } from "react-toastify";
import request from '../services/requestService';
import Form from "../base/form";
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import 'bootstrap/dist/css/bootstrap.min.css';



class DeleteData extends Form {
    state = {
        data: { ...this.props.data },
        errors: {},
        show: false,
        buttonDisabled: false,
    };

    schema = { ...this.props.schema };

    handleClose = () => {
        this.setState({ show: false });
    }

    handleShow = () => {
        this.setState({ show: true });
    }


    formData(item) {
        return this.renderInput(item.name, item.label, item.type);
    }


    onSubmit(data) {
        return this.deleteData(data);
    }


    deleteData = async (data) => {
        try {
            const response = request.deleteObject(this.props.id, this.props.urlDelete, data);
            console.log(response);

            toast.promise(
                response.then(() => new Promise(resolve => setTimeout(resolve, 200))),
                {
                    pending: 'Loading...',
                    success: { render: `id ${this.props.id} Was Deleted!`, type: "info", autoClose: 2800 },
                    error: 'Promise rejected 🤯'
                }
            );

            await new Promise(resolve => setTimeout(resolve, 2500))

            if (this.props.toPath) return window.location.replace(this.props.toPath);
            else return window.location.replace(this.props.location.pathname.replace(`/${this.props.id}`, ""));
        } catch (error) {
            console.log(error);
            toast.error(error.message);
        }
    }

    // props = {
    //     data,
    //     schema,
    //     formData,
    //     urlDelete,
    //     toPath,
    //     id,
    //     location,
    //     navigate,
    //     doSubmit,
    //     title,
    //     body,
    //     label
    // }
    


    render() {
        var label = this.props.label ? this.props.label : "Delete";
        var className = this.props.className ? this.props.className : "btn btn-danger primary";
        var title = this.props.title ? this.props.title : "Delete";
        var body = this.props.body ? this.props.body : "Are you sure you want to delete this item?";

        return (
            <>
                <Button variant={className} onClick={this.handleShow}>
                    {label}
                </Button>

                <Modal show={this.state.show} onHide={this.handleClose} animation={false} >
                    <Modal.Header>
                        <Modal.Title>{title}</Modal.Title>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close" onClick={this.handleClose}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
                                <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708" />
                            </svg>
                        </button>

                    </Modal.Header>
                    <form onSubmit={this.handleSubmit}>
                        <Modal.Body>
                            {body}
                            {this.props.formData ? this.props.formData.map(item => this.formData(item)) : ""}
                        </Modal.Body>

                        <Modal.Footer>
                            <Button variant="secondary" onClick={this.handleClose}>
                                Close
                            </Button>
                            {this.renderButton(label, this.buttonDisabled, className)}
                        </Modal.Footer>
                    </form>
                </Modal>
            </>

        );
    }
}

export default DeleteData;
