import "/ADC_sampling/adc_sampler.c"

static PyObject * adc_sampler_wrapper(PyObject * self, PyObject *args) {
	char * input; 
	//char * result; 
	//PyObject * ret; 

	//parse arguments
	if (!PyArg_ParseTuple(args, "i", &input)) {
		return NULL; 
	}
	
	//Run the function
	main(args)
		
		
