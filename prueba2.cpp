#include <iostream>

using namespace std;

int main(){
    int a = 5;
    int b = 15;
    int d = a + b;
    int e = b - a;
    int f = a * b;
    int g = b / a;

    cout << "Hola Mundo" << endl;
    cout << "Esta funcionando?" << endl;
    cout << "La Suma es " << endl;
    cout << d << endl;
    cout << "La Resta es " << endl;
    cout << e << endl;
    cout << "La Multiplicacion es " << endl;
    cout << f << endl;
    cout << "La Division es " << endl;
    cout << g << endl;

    if(a < 10){
        cout << "Hola, si funciona" << endl;
    }


    return 0;
}