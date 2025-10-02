package main

import (
	"fmt"
	"net"
	"os"
	"strings"
	"time"
)

func handleConnection(c net.Conn) {
	time.Sleep(30 * time.Second)

	// Attempt to send FIN/ACK rather than RST
	buf := make([]byte, 4096)
	c.Read(buf)

	c.Close()
}

func main() {
	arguments := os.Args
	if len(arguments) < 3 {
		fmt.Println("Usage: ./server ip:port ip_of_client")
		return
	}
	ADDR := arguments[1]
	client_ip := arguments[2]

	l, err := net.Listen("tcp4", ADDR)
	if err != nil {
		fmt.Println(err)
		return
	}

	defer l.Close()

	for {
		c, err := l.Accept()
		c.SetReadDeadline(time.Now().Add(time.Duration(30) * time.Second))
		if err != nil {
			fmt.Println(err)
			return
		}

		ip := strings.Split(c.RemoteAddr().String(), ":")[0]
		if ip != client_ip {
			fmt.Print(time.Now().Format("2006-01-02 15:04:05"))
			fmt.Println(" Unrecognized SrcIP: ", ip)
		}
		go handleConnection(c)
	}
}
