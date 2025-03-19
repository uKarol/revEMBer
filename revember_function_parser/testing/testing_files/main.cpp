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
static err_t low_level_output(struct netif *netif, struct pbuf *p)
{
  uint32_t i = 0U;
  struct pbuf *q = NULL;
  err_t errval = ERR_OK;
  ETH_BufferTypeDef Txbuffer[ETH_TX_DESC_CNT] = {0};

  memset(Txbuffer, 0 , ETH_TX_DESC_CNT*sizeof(ETH_BufferTypeDef));

  for(q = p; q != NULL; q = q->next)
  {
    if(i >= ETH_TX_DESC_CNT)
      return ERR_IF;

    Txbuffer[i].buffer = q->payload;
    Txbuffer[i].len = q->len;

    if(i>0)
    {
      Txbuffer[i-1].next = &Txbuffer[i];
    }

    if(q->next == NULL)
    {
        if(i >= ETH_TX_DESC_CNT) return ERR_IF;
    }

    i++;
  }

  TxConfig.Length = p->tot_len;
  TxConfig.TxBuffer = Txbuffer;
  TxConfig.pData = p;

  HAL_ETH_Transmit(&heth, &TxConfig, ETH_DMA_TRANSMIT_TIMEOUT);

  return errval;
}


/* DZIWNE FUNKCJE */

void pattern1 (int x, int y) {std::cout<<"pattern1";}
void pattern2(int x, int y){
  
 
std::cout<<"pattern2";
 
  
}

void pattern3(int x, int y){
  
 
    std::cout<<"pattern3";
 
  
}

err_t
udp_send_chksum(struct udp_pcb *pcb, struct pbuf *p,
                u8_t have_chksum, u16_t chksum){
    
    if(pcb == NULL)
    return udp_sendto_chksum(pcb, p, &pcb->remote_ip, pcb->remote_port,
        have_chksum, chksum);

    return 0;
}

err_t
udp_send_chksum(struct udp_pcb *pcb, struct pbuf *p,
                u8_t have_chksum, u16_t chksum){
  
    return udp_sendto_chksum(pcb, p, &pcb->remote_ip, pcb->remote_port,
        have_chksum, chksum);
}

err_t
netconn_recv_tcp_pbuf_flags(struct netconn *conn, struct pbuf **new_buf, u8_t apiflags)
{
  LWIP_ERROR("netconn_recv_tcp_pbuf: invalid conn", (conn != NULL) &&
             NETCONNTYPE_GROUP(netconn_type(conn)) == NETCONN_TCP, return ERR_ARG;);

  return netconn_recv_data_tcp(conn, new_buf, apiflags);
}

err_t
netconn_getaddr pattern5(int x, int y)
{
    std::cout<<"pattern5";
    LWIP_ERROR("netconn_getaddr: invalid conn", (conn != NULL), return ERR_ARG;);
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
