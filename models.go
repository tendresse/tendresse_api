package main

type Gif struct {
	gorm.Model
	ID uint
	Url string
	LameScore uint
	Tags []Tag `gorm:"many2many:gif_tags;"`
}

type Sucess struct {
	gorm.Model
    ID uint
    Title string
    Tags []Tag `gorm:"many2many:success_tags;"`
    Condition uint
    TypeOf string
    Icon string
}

type Tag struct {
	gorm.Model
    ID uint
    Name string `gorm:"not null;unique"`
}

type Tendresse struct {
	gorm.Model
    ID uint
    SenderID uint
    Sender User
    ReceivedID uint
    Receiver User
    GifID uint
    Gif Gif
    StateViewed bool
}

type User struct {
	gorm.Model
    ID uint
    Username string
    Password string
    Friends []User `gorm:"many2many:user_friends;"`
    Achievements []Success `gorm:"many2many:user_successes;"`
    Device string
    Role string
}