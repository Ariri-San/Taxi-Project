import GetForm from "./getForm.jsx";

class FormDjango extends GetForm {

    state = {
        data: {},
        errors: {},
        optionsData: {},
        buttonDisabled: false,
    };

    schema = {};



    // props = {
    //     buttonName,
    //     urlForm,
    //     id,
    //     onResults(data, results),
    //     onSubmit(this.state),
    //     data,
    //     optionsData,   // optionsData={[{object: "text", key: ["username", "type"]}]}
    //     schema,   // schema={[{ object: Joi.string().label("Password").required().min(8), key: ['user', 'password'] }]}
    //     navigate,
    //     location,
    //     label,
    // }


    render() {
        if (Object.keys(this.state.data).length)
            return (
                <>
                    {this.props.label && <h1>{this.props.label}</h1>}
                    {this.getFormData(this.props.buttonName ? this.props.buttonName : "Submit")}
                </>
            );
    }
}

export default FormDjango;