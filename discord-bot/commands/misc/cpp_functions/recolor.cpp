//cppimport
#include <pybind11/pybind11.h>

#include <vector>
#include <string>
#include <cmath>
#include <typeinfo>

namespace py = pybind11;

py::bytes recolor(std::string img, unsigned int height, unsigned int width, unsigned char r, unsigned char g, unsigned char b, float intensity){
	//create vector of prescaled target rgb
	std::vector<unsigned char> rgb = {r, g, b};

	for(size_t i = 0; i<width*height*4; i++){
		if(i%4!=3){
			unsigned char *p = reinterpret_cast<unsigned char*>(&img[i]);
			signed int part = *p + ((signed int) *p * ((float)(rgb[i%4]-*p)/255)*intensity);
			img[i] = part;
		}
	}
	return(img);
}

PYBIND11_MODULE(recolor, m){
    m.doc() = "recolor images in cpp";
    m.def("recolor", &recolor);
}

/*
<%
setup_pybind11(cfg)
%>
*/
