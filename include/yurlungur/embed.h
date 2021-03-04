//
// Created by sho sumioka on 西暦 2019/10/29.
//

#ifndef YURLUNGUR_EMBED_H
#define YURLUNGUR_EMBED_H

//https://pybind11.readthedocs.io/en/stable/classes.html
#include <pybind11/pybind11.h>

struct Pet {
    enum Kind {
        Dog = 0,
        Cat
    };

    Pet(const std::string &name, Kind type) : name(name), type(type) {}

    std::string name;
    Kind type;
};

#endif //YURLUNGUR_EMBED_H
