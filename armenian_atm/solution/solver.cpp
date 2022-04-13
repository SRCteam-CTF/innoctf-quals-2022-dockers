#include <iostream>
#include <string>
#include <time.h>
#include <vector>

using namespace std;

const string alphabet = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890+/";

int main() {
    int ts;
    cin >> ts;
    srand(ts);

    vector<unsigned char> tmp;
    for (int i = 0; i < 33; i++){
        unsigned char x = rand() % 256;
        tmp.push_back(x);
    }
    string code = "";

    for (int i = 0; i < 33; i+=3){
        int n1 = (tmp[i] >> 2) & 63;
        int n2 = ((tmp[i] & 3) << 4) | ((tmp[i+1] >> 4) & 15);
        int n3 = ((tmp[i+1] & 15) << 2) | ((tmp[i+2] >> 6) & 3);
        int n4 = tmp[i+2] & 63;
        code += alphabet[n1];
        code += alphabet[n2];
        code += alphabet[n3];
        code += alphabet[n4];
    }
    cout << code << endl;
    return 0;
}
