#include <iostream>

typedef struct {
    int dupa1;
    float dziadostwo;
}always_problem;

struct {
    int numer;
}xd_duo;

char nutnut[] =
{
    3,
    5,
    7,
    9,
};

int t[5] {
    4,
    6,
    7,
    8,
    0,
};

int get_trash(){return 0;}

int get_trash1(){
    return 1;}

/* dziadostwo */
void put_trash(){
std::cout<<"dupa";  
}

static 
volatile 
int 
intializer  
(   /* kto tak zjebal */
    int x 
) /*
co to*/
{
    x = 1000;
    x++;
   // std::cout<< x;
    return x;
}
/*
    to 
    kjest 
    glowna
*/
int main(){
    xd_duo;
    int x = 0;
    x = intializer(0);
    float z{5};
    int y{6};
    std::cout << "Hello World" << x << " " << y <<std::endl; 
}
/*
    nie wiem co to
*/


/* DZIWNE FUNKCJE */

void pattern1 (int x, int y) {std::cout<<"pattern1";}
void pattern2(int x, int y){
  
 
std::cout<<"pattern2";
 
  
}

void pattern3(int x, int y){
  
 
    std::cout<<"pattern3";
 
  
}

void pattern4(int x, int y){
  
 
    std::cout<<"pattern4";
 
  
}

void pattern5(int x, int y)
{
    std::cout<<"pattern5";
}

void pattern6(int x, int y
)
{
    std::cout<<"pattern6";
}

void pattern7(int x, 
    int y
)
{  std::cout<<"pattern7";
  
}

void pattern8(
    int x, 
    int y
)
{
  std::cout<<"pattern8";
}

static void (pattern9)
(
    int x, 
    int y
)
{
    std::cout<<"pattern9";
  
}

int dupa (int (*paIndex)[3] , int (* fpMsg) (const char *), int (* fpCalculation[3]) (const char *)); 
//{ 
    //*fpData++; 
    //return NULL;
//}
