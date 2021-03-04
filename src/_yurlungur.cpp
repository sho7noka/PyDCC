//
// Created by sho sumioka on 西暦 2020/03/14.
//
#include <yurlungur/embed.h>

namespace py = pybind11;

PYBIND11_MODULE(yurlungur, m) {
    py::class_ <Pet> pet(m, "Pet");

    pet.

    def (py::init<const std::string &, Pet::Kind>())

    .def_readwrite("name", &Pet::name)
    .def_readwrite("type", &Pet::type);

    py::enum_<Pet::Kind>(pet,
    "Kind")
    .value("Dog", Pet::Kind::Dog)
    .value("Cat", Pet::Kind::Cat)
    .export_values();
}