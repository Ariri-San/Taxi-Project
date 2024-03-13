import React, { Component } from "react";
import Joi from "joi-browser";
import Input from "./input";
import Select from "./select";
import TextArea from "./textArea";
import { toast } from "react-toastify";
import request from "../services/requestService.js";

class Form extends Component {
    state = {
        data: {},
        errors: {},
    };


    doSubmit = async (data) => {
        if (this.props.onSubmit) return this.props.onSubmit(this.state);
        else if ( this.onSubmit) return this.onSubmit(data);

        try {
            const response = request.saveObject(this.setFormData(data, new FormData()), this.props.urlForm, this.props.id);
            
            this.buttonDisabled = true;
            const results = await response;

            toast.promise(
                response.then(() => new Promise(resolve => setTimeout(resolve, 300))),
                {
                    pending: 'Loading...',
                    success: { render: `${results.data.id ? `Id: ${results.data.id}, ` : ""}message: ${results.statusText}`, autoClose: 1500 },
                    error: `${results.statusText} 🤯`
                }
            );

            // console.log(results);

            await new Promise(resolve => setTimeout(resolve, 2000))
            this.buttonDisabled = false;
            if (this.props.onResults) {
                this.props.onResults(data, results);
            }

            return this.props.navigate(this.props.toPath);

        } catch (error) {
            if (error.response){
                console.log(error)
                if (error.response.data) {
                    const errorData = this.addErrors(error.response.data, {}), newError = {}
                    if (errorData["key"] === "0") toast.error(errorData["value"][0]);
                    else newError[errorData["key"]] = errorData["value"];
                    this.setState({ errors: newError });
    
                    // console.log(error);
                    toast.error(error.response.statusText);
                };
    
                await new Promise(resolve => setTimeout(resolve, 500))
                this.buttonDisabled = false;
                this.props.navigate();
            }
            else {
                this.buttonDisabled = false;
                return toast.error("server is ofline");
            }
        }
    };


    setFormData(data, formData, addKey = "") {
        for (const key in data) {
            // console.log(key, data[key]);

            if (typeof data[key] === "object" && data[key]) {
                if (Object.keys(data[key]).length > 0) {
                    this.setFormData(data[key], formData, addKey + key + ".");
                }
                else if (data[key]) formData.append(addKey + key, data[key]);  // this is file
            }
            else if (data[key]) formData.append(addKey + key, data[key]);   // this is string

        }

        return formData;
    }


    addErrors(error, new_error) {
        if (Array.isArray(error))
            return {
                "key": Object.keys(error)[0],
                "value": error
            };
        for (const key in error) {
            if (key === "detail") return toast.error(error.detail)
            if (Object.hasOwnProperty.call(error, key)) {
                if (Array.isArray(error[key]))
                    return {
                        "key": Object.keys(error)[0],
                        "value": error[key]
                    };
                if (Object.keys(error[key])) {
                    const error_2 = this.addErrors(error[key]);
                    return {
                        "key": Object.keys(error)[0] + "." + error_2["key"],
                        "value": error_2["value"]
                    };
                }
            }
        }
        return error;
    }



    updateNestedValue(obj, keys, newValue) {
        var obj_2 = obj;

        for (let index = 0; index < keys.length - 1; index++) {
            obj_2 = obj_2[keys[index]];
        }

        obj_2[keys[keys.length - 1]] = newValue;

        return obj;
    }


    validate = () => {
        const options = { abortEarly: false };
        const { error } = Joi.validate(this.state.data, this.schema, options);
        if (!error) return null;

        const errors = {};
        for (let item of error.details) errors[item.path[0]] = item.message;
        return errors;
    };

    validateProperty = ({ name, value }) => {
        const obj = { [name]: value };
        const array = name.split(".");
        var schema = this.schema;
        for (let index = 0; index < array.length; index++) {
            schema = schema[array[index]];
        }

        schema = { [name]: schema };
        const { error } = Joi.validate(obj, schema);
        return error ? error.details[0].message : null;
    };

    handleSubmit = e => {
        e.preventDefault();

        const errors = this.validate();
        this.setState({ errors: errors || {} });
        if (errors) return;

        var data = { ...this.state.data };
        for (const input of e.target) {
            if (input.type === "file") {
                data = this.updateNestedValue(data, input.name.split("."), input.files[0]);
            }
        }

        this.doSubmit(data);
    };

    handleChange = ({ currentTarget: input }) => {
        var value = input.value;
        if (input.type === "checkbox") value = input.checked;

        const errors = { ...this.state.errors };
        const errorMessage = this.validateProperty(input);
        if (errorMessage) errors[input.name] = errorMessage;
        else delete errors[input.name];

        var data = { ...this.state.data };
        data = this.updateNestedValue(data, input.name.split("."), value);

        this.setState({ data, errors });
    };

    renderButton(label, disabled = false, className = "btn btn-primary") {
        return (
            <button disabled={this.validate() || disabled} className={className}>
                {label}
            </button>
        );
    }

    renderSelect(name, label, options) {
        const { data, errors } = this.state;

        return (
            <Select
                key={name}
                name={name}
                value={data[name]}
                label={label}
                options={options}
                onChange={this.handleChange}
                error={errors[name]}
            />
        );
    }

    renderInput(name, label, type = "text", list = "") {
        const { data, errors } = this.state;

        return (
            <Input
                key={name}
                type={type}
                name={name}
                value={data[name]}
                label={label}
                list={list}
                onChange={this.handleChange}
                error={errors[name]}
            />
        );
    }

    renderTextArea(name, label) {
        const { data, errors } = this.state;

        return (
            <TextArea
                key={name}
                name={name}
                value={data[name]}
                label={label}
                onChange={this.handleChange}
                error={errors[name]}
            />
        );
    }


}



export default Form;
