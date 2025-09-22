import requests
import random
import os
import time

cluster_domain = os.environ.get('CLUSTERDOMAIN', '')

PLAYER_COUNT = 100

bottle_message = ["                                                                                                                                                                                                                                                                                                                                                                                                                      ",
                  "                                                                                                                                                                                            dddddddd                                                                                                                                                                                                                  ",
                  "TTTTTTTTTTTTTTTTTTTTTTThhhhhhh                                         ffffffffffffffff  lllllll                                                                                            d::::::d                           iiii                                GGGGGGGGGGGGG                  lllllll                                                                                                             ",
                  "T:::::::::::::::::::::Th:::::h                                        f::::::::::::::::f l:::::l                                                                                            d::::::d                          i::::i                            GGG::::::::::::G                  l:::::l                                                                                                             ",
                  "T:::::::::::::::::::::Th:::::h                                       f::::::::::::::::::fl:::::l                                                                                            d::::::d                           iiii                           GG:::::::::::::::G                  l:::::l                                                                                                             ",
                  "T:::::TT:::::::TT:::::Th:::::h                                       f::::::fffffff:::::fl:::::l                                                                                            d:::::d                                                          G:::::GGGGGGGG::::G                  l:::::l                                                                                                             ",
                  "TTTTTT  T:::::T  TTTTTT h::::h hhhhh           eeeeeeeeeeee          f:::::f       ffffff l::::l   aaaaaaaaaaaaa     ggggggggg   ggggg         cccccccccccccccc   ooooooooooo       ddddddddd:::::d     eeeeeeeeeeee         iiiiiii     ssssssssss         G:::::G       GGGGGG  aaaaaaaaaaaaa    l::::l   aaaaaaaaaaaaa  ppppp   ppppppppp     aaaaaaaaaaaaa     ggggggggg   ggggg   ooooooooooo       ssssssssss   ",
                  "        T:::::T         h::::hh:::::hhh      ee::::::::::::ee        f:::::f              l::::l   a::::::::::::a   g:::::::::ggg::::g       cc:::::::::::::::c oo:::::::::::oo   dd::::::::::::::d   ee::::::::::::ee       i:::::i   ss::::::::::s       G:::::G                a::::::::::::a   l::::l   a::::::::::::a p::::ppp:::::::::p    a::::::::::::a   g:::::::::ggg::::g oo:::::::::::oo   ss::::::::::s  ",
                  "        T:::::T         h::::::::::::::hh   e::::::eeeee:::::ee     f:::::::ffffff        l::::l   aaaaaaaaa:::::a g:::::::::::::::::g      c:::::::::::::::::co:::::::::::::::o d::::::::::::::::d  e::::::eeeee:::::ee      i::::i ss:::::::::::::s      G:::::G                aaaaaaaaa:::::a  l::::l   aaaaaaaaa:::::ap:::::::::::::::::p   aaaaaaaaa:::::a g:::::::::::::::::go:::::::::::::::oss:::::::::::::s ",
                  "        T:::::T         h:::::::hhh::::::h e::::::e     e:::::e     f::::::::::::f        l::::l            a::::ag::::::ggggg::::::gg     c:::::::cccccc:::::co:::::ooooo:::::od:::::::ddddd:::::d e::::::e     e:::::e      i::::i s::::::ssss:::::s     G:::::G    GGGGGGGGGG           a::::a  l::::l            a::::app::::::ppppp::::::p           a::::ag::::::ggggg::::::ggo:::::ooooo:::::os::::::ssss:::::s",
                  "        T:::::T         h::::::h   h::::::he:::::::eeeee::::::e     f::::::::::::f        l::::l     aaaaaaa:::::ag:::::g     g:::::g      c::::::c     ccccccco::::o     o::::od::::::d    d:::::d e:::::::eeeee::::::e      i::::i  s:::::s  ssssss      G:::::G    G::::::::G    aaaaaaa:::::a  l::::l     aaaaaaa:::::a p:::::p     p:::::p    aaaaaaa:::::ag:::::g     g:::::g o::::o     o::::o s:::::s  ssssss ",
                  "        T:::::T         h:::::h     h:::::he:::::::::::::::::e      f:::::::ffffff        l::::l   aa::::::::::::ag:::::g     g:::::g      c:::::c             o::::o     o::::od:::::d     d:::::d e:::::::::::::::::e       i::::i    s::::::s           G:::::G    GGGGG::::G  aa::::::::::::a  l::::l   aa::::::::::::a p:::::p     p:::::p  aa::::::::::::ag:::::g     g:::::g o::::o     o::::o   s::::::s      ",
                  "        T:::::T         h:::::h     h:::::he::::::eeeeeeeeeee        f:::::f              l::::l  a::::aaaa::::::ag:::::g     g:::::g      c:::::c             o::::o     o::::od:::::d     d:::::d e::::::eeeeeeeeeee        i::::i       s::::::s        G:::::G        G::::G a::::aaaa::::::a  l::::l  a::::aaaa::::::a p:::::p     p:::::p a::::aaaa::::::ag:::::g     g:::::g o::::o     o::::o      s::::::s   ",
                  "        T:::::T         h:::::h     h:::::he:::::::e                 f:::::f              l::::l a::::a    a:::::ag::::::g    g:::::g      c::::::c     ccccccco::::o     o::::od:::::d     d:::::d e:::::::e                 i::::i ssssss   s:::::s       G:::::G       G::::Ga::::a    a:::::a  l::::l a::::a    a:::::a p:::::p    p::::::pa::::a    a:::::ag::::::g    g:::::g o::::o     o::::ossssss   s:::::s ",
                  "      TT:::::::TT       h:::::h     h:::::he::::::::e               f:::::::f            l::::::la::::a    a:::::ag:::::::ggggg:::::g      c:::::::cccccc:::::co:::::ooooo:::::od::::::ddddd::::::dde::::::::e               i::::::is:::::ssss::::::s       G:::::GGGGGGGG::::Ga::::a    a:::::a l::::::la::::a    a:::::a p:::::ppppp:::::::pa::::a    a:::::ag:::::::ggggg:::::g o:::::ooooo:::::os:::::ssss::::::s",
                  "      T:::::::::T       h:::::h     h:::::h e::::::::eeeeeeee       f:::::::f            l::::::la:::::aaaa::::::a g::::::::::::::::g       c:::::::::::::::::co:::::::::::::::o d:::::::::::::::::d e::::::::eeeeeeee       i::::::is::::::::::::::s         GG:::::::::::::::Ga:::::aaaa::::::a l::::::la:::::aaaa::::::a p::::::::::::::::p a:::::aaaa::::::a g::::::::::::::::g o:::::::::::::::os::::::::::::::s ",
                  "      T:::::::::T       h:::::h     h:::::h  ee:::::::::::::e       f:::::::f            l::::::l a::::::::::aa:::a gg::::::::::::::g        cc:::::::::::::::c oo:::::::::::oo   d:::::::::ddd::::d  ee:::::::::::::e       i::::::i s:::::::::::ss            GGG::::::GGG:::G a::::::::::aa:::al::::::l a::::::::::aa:::ap::::::::::::::pp   a::::::::::aa:::a gg::::::::::::::g  oo:::::::::::oo  s:::::::::::ss  ",
                  "      TTTTTTTTTTT       hhhhhhh     hhhhhhh    eeeeeeeeeeeeee       fffffffff            llllllll  aaaaaaaaaa  aaaa   gggggggg::::::g          cccccccccccccccc   ooooooooooo      ddddddddd   ddddd    eeeeeeeeeeeeee       iiiiiiii  sssssssssss                 GGGGGG   GGGG  aaaaaaaaaa  aaaallllllll  aaaaaaaaaa  aaaap::::::pppppppp      aaaaaaaaaa  aaaa   gggggggg::::::g    ooooooooooo     sssssssssss    ",
                  "                                                                                                                              g:::::g                                                                                                                                                                                       p:::::p                                         g:::::g                                   ",
                  "                                                                                                                  gggggg      g:::::g                                                                                                                                                                                       p:::::p                             gggggg      g:::::g                                   ",
                  "                                                                                                                  g:::::gg   gg:::::g                                                                                                                                                                                      p:::::::p                            g:::::gg   gg:::::g                                   ",
                  "                                                                                                                   g::::::ggg:::::::g                                                                                                                                                                                      p:::::::p                             g::::::ggg:::::::g                                   ",
                  "                                                                                                                    gg:::::::::::::g                                                                                                                                                                                       p:::::::p                              gg:::::::::::::g                                    ",
                  "                                                                                                                      ggg::::::ggg                                                                                                                                                                                         ppppppppp                                ggg::::::ggg                                      ",
                  "                                                                                                                         gggggg                                                                                                                                                                                                                                        gggggg                                         "]


bottle_coords = [(x, y) for x,
                 chosen_str in enumerate(bottle_message) for y,
                 char in enumerate(chosen_str) if char.strip()]


def pick_bottle_char():
    y, x = random.choice(bottle_coords)
    char = bottle_message[y][x]
    return char, x, y


def post_json_and_forget(url, data):

    try:
        print(f"HTTP POST: {url}")
        response = requests.post(url, json=data)
        print(response)
        
        if response.status_code == 200:
            print(f"{response.status_code} - bottle succesfully received")
        elif response.status_code == 503:
            print(f"{response.status_code} - player API endpoint not responsing yet")
        else:
            print(f"An unexpected error occurred: {response.status_code}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")




def challenge_bottle():

    # Randomly choose between 10 to 100 bottles
    num_bottles = random.randint(10, 200)
    bottles = []

    for _ in range(num_bottles):
        char, x, y = pick_bottle_char()
        bottle_data = {
            'character': char,
            'coordinates': {'x': x, 'y': y}
        }
        bottles.append(bottle_data)

    for i in range(1, PLAYER_COUNT + 1):
        url = f"https://bottles-player{i}.apps.{cluster_domain}/collect-bottles"
        post_json_and_forget(url, bottles)
        time.sleep(0.05)


def main():

    while True:
        challenge_bottle()


if __name__ == "__main__":
    main()
