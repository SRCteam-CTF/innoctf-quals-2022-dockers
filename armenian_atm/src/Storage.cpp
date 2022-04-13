#include "./Storage.hpp"

Storage::Storage(){
    std::ifstream secret_f("flag.txt");
    if (secret_f.is_open()) {
        std::string line;
        getline(secret_f, line);
        this->secret = line;
    } else {
        this->secret = "secret";
    }
}