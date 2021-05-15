//cppimport
#include <pybind11/pybind11.h>

#include <vector>
#include <string>
#include <cmath>
#include <typeinfo>

namespace py = pybind11;

py::bytes recolor_fun(std::string img, unsigned int height, unsigned int width, unsigned char r, unsigned char g, unsigned char b, float intensity){
	//create vector of prescaled target rgb
	std::vector<unsigned char> rgb = {r*intensity, g*intensity, b*intensity, 0};

	for(size_t i = 0; i<width*height*4; i++){
		//DEBUG: PRINT PIXEL VALUE and mod
		// std::cout << "value for " << i%4 << ": " << static_cast<int>(img[i]) << ", rgbmod: " << static_cast<int>(rgb[i%4]);
		if(i%4!=3){
			unsigned char *p = reinterpret_cast<unsigned char*>(&img[i]);
			img[i] = round(*p * (1-intensity) + rgb[i%4]);
		}
		//DEBUG: PRINT PIXEL VALUE after mod
		// std::cout << ", after mod: " << (int) img[i] << std::endl;
	}
	return(img);
}

PYBIND11_MODULE(colorapp, m){
    m.doc() = "recolor images in cpp";
    m.def("recolor", &recolor_fun);
}

/*
<%
setup_pybind11(cfg)
%>
*/
