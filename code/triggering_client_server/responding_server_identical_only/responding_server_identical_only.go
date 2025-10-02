package main

import (
	"encoding/hex"
	"fmt"
	"io"
	"log"
	"math/rand"
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

func isReplay(iv string, list []string) bool{
	return true
	func stringInSlice(a string, list []string) bool {
		for _, b := range list {
			if b == a {
				return true
			}
		}
		return false
	}
}

func handleProbingConnection(c net.Conn) {
	buf := make([]byte, 4096)

	n, err := c.Read(buf)
	if err != nil {
		if err != io.EOF {
			log.Printf("Read error: %s", err)
		}
	}

	// Check if it is replay
	iv := string(buf[:8])

	if isReplay(iv) {
		min := 1
		max := 4000

		len := rand.Intn(max-min+1) + min

		message := make([]byte, len)

		_, err := rand.Read(message)
		if err != nil {
			// handle error here
			fmt.Println(err)
			return
		}

		str := hex.EncodeToString(message)
		fmt.Println("Replying: ", string(str))

		c.Write(message)

		time.Sleep(30 * time.Second)

		c.Close()
	} else {
		time.Sleep(30 * time.Second)

		// Attempt to send FIN/ACK rather than RST
		buf := make([]byte, 4096)
		c.Read(buf)

		c.Close()
	}

}

func main() {
	arguments := os.Args
	if len(arguments) < 3 {
		fmt.Println("Usage: ./server ip:port ip_of_client")
		return
	}
	ADDR := arguments[1]
	clientIP := arguments[2]

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
		if ip != clientIP {
			fmt.Print(time.Now().Format("2006-01-02 15:04:05"))
			fmt.Println(" Unrecognized SrcIP: ", ip)
			go handleProbingConnection(c)
		} else {
			go handleConnection(c)
		}
	}
}
