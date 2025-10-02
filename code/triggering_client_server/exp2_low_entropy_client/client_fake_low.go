package main

import (
	"bytes"
	"encoding/hex"
	"fmt"
	"math/rand"
	"net"
	"os"
	"time"
)

func sendMessage(c net.Conn, len int) {
	const uniqNum = 3

	message := make([]byte, uniqNum)

	_, err := rand.Read(message)
	if err != nil {
		// handle error here
		fmt.Println(err)
		return
	}

	// fmt.Println(len)

	message = bytes.Repeat(message, len)[:len]

	str := hex.EncodeToString(message)
	fmt.Println(string(str))

	// send to socket
	c.Write(message)

	// listen for reply
	// message, _ := bufio.NewReader(conn).ReadString('\n')
	// fmt.Print("Message from server: " + message)
}

func main() {

	arguments := os.Args
	if len(arguments) == 1 {
		fmt.Println("Please provide a ip:port pair!")
		return
	}
	ADDR := arguments[1]

	seed := time.Now().UTC().UnixNano()
	rand.Seed(seed)

	min := 1
	max := 1000

	for {
		// connect to this socket
		len := rand.Intn(max-min+1) + min

		conn, err := net.Dial("tcp", ADDR)
		if err != nil {
			// handle error here
			fmt.Println(err)
			continue
		}

		go sendMessage(conn, len)

		time.Sleep(1 * time.Second)
	}
}
