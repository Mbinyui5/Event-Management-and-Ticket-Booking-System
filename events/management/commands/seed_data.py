import uuid
from datetime import date, time, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from events.models import Category, Event
from bookings.models import Booking, Ticket

class Command(BaseCommand):
    help = 'Seeds the database with Cameroon-localized Categories, Users, Events, and Bookings.'

    def handle(self, *args, **options):
        self.stdout.write("Starting database seeding (Cameroon Localized)...")

        # 1. Clean existing database records
        self.stdout.write("Cleaning database tables...")
        Ticket.objects.all().delete()
        Booking.objects.all().delete()
        Event.objects.all().delete()
        Category.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        User.objects.filter(username='admin').delete()

        # 2. Create Categories
        self.stdout.write("Creating event categories...")
        categories = {
            'music': Category.objects.create(name="Music Festivals", description="Live music, Makossa, Bikutsi, Afro-jazz concert events."),
            'tech': Category.objects.create(name="Silicon Mountain & Tech", description="Coding workshops, tech exhibitions, and developer forums."),
            'sports': Category.objects.create(name="Sports & Tournaments", description="Football matches, Mt. Cameroon Race of Hope events, and athletic events."),
            'arts': Category.objects.create(name="Arts & Culture", description="Traditional dance galas, craft displays, and museum excursions."),
            'business': Category.objects.create(name="Business & Seminars", description="Networking dinners, investment panels, and commercial expos."),
            'education': Category.objects.create(name="Education & Training", description="Academic workshops, university seminars, and career fairs."),
            'gaming': Category.objects.create(name="Gaming & eSports", description="Video game tournaments, LAN parties, and esports competitions."),
            'health': Category.objects.create(name="Health & Wellness", description="Fitness classes, health awareness campaigns, and wellness retreats."),
        }

        # 3. Create Users
        self.stdout.write("Creating seed users...")
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@eventpass.cm',
            password='adminpassword',
            first_name='Admin',
            last_name='User'
        )

        attendee1 = User.objects.create_user(
            username='john',
            email='john@example.cm',
            password='password123',
            first_name='John',
            last_name='Ndi'
        )
        attendee1.profile.phone_number = "+237677123456"
        attendee1.profile.save()

        attendee2 = User.objects.create_user(
            username='jane',
            email='jane@example.cm',
            password='password123',
            first_name='Jane',
            last_name='Foning'
        )
        attendee2.profile.phone_number = "+237699654321"
        attendee2.profile.save()

        attendee3 = User.objects.create_user(
            username='mike',
            email='mike@example.cm',
            password='password123',
            first_name='Michael',
            last_name='Tchakounté'
        )
        attendee3.profile.save()

        attendee4 = User.objects.create_user(
            username='sarah',
            email='sarah@example.cm',
            password='password123',
            first_name='Sarah',
            last_name='Mbah'
        )
        attendee4.profile.phone_number = "+237677987654"
        attendee4.profile.save()

        attendee5 = User.objects.create_user(
            username='paul',
            email='paul@example.cm',
            password='password123',
            first_name='Paul',
            last_name='Fokam'
        )
        attendee5.profile.save()
        self.stdout.write("-> Created superuser: 'admin' and Cameroonian attendee accounts: 'john', 'jane', 'mike', 'sarah', 'paul'")

        # 4. Create Events
        self.stdout.write("Creating mock Cameroonian events...")
        today = date.today()

        # ============================
        # MUSIC EVENTS
        # ============================

        event1 = Event.objects.create(
            title="Mboa Jazz & Makossa Festival",
            description="A premium gathering of legendary Makossa icons and modern Afro-jazz artists. Enjoy local culinary delicacies, fresh fish from Down Beach, and live bands performing under the stars in Douala.",
            category=categories['music'],
            date=today + timedelta(days=15),
            time=time(18, 0),
            venue="Canal Olympia, Douala",
            capacity=150,
            ticket_price=10000.00,
            status='published',
            created_by=admin_user
        )

        event9 = Event.objects.create(
            title="Bamenda Acoustic Night",
            description="An intimate evening of live acoustic performances by talented local artists. Enjoy soulful music, warm drinks, and cultural vibes in the heart of Bamenda city.",
            category=categories['music'],
            date=today + timedelta(days=5),
            time=time(19, 0),
            venue="Commercial Avenue Cultural Center, Bamenda",
            capacity=120,
            ticket_price=3000.00,
            status='published',
            created_by=admin_user
        )

        event10 = Event.objects.create(
            title="Abakwa Music Fest",
            description="A grand celebration of the vibrant musical heritage of Bamenda. Featuring traditional folk music, modern Afro-pop, and live instrumental bands representing the rich North-West culture.",
            category=categories['music'],
            date=today + timedelta(days=22),
            time=time(16, 0),
            venue="Mankon Cultural Center, Bamenda",
            capacity=250,
            ticket_price=5000.00,
            status='published',
            created_by=admin_user
        )

        event_music_gospel = Event.objects.create(
            title="Cameroon Gospel Praise Night",
            description="A powerful evening of gospel music featuring top gospel artists from across Cameroon. A night of worship, praise, and uplifting spiritual music that will leave you refreshed.",
            category=categories['music'],
            date=today + timedelta(days=7),
            time=time(18, 30),
            venue="Palais des Sports, Yaoundé",
            capacity=500,
            ticket_price=1500.00,
            status='published',
            created_by=admin_user
        )

        event_music_bikutsi = Event.objects.create(
            title="Bikutsi Rhythm Gala",
            description="Celebrate the thunderous Bikutsi genre with top Beti performers. Dance to the infectious rhythms of this UNESCO-recognized Cameroonian musical art form in a colorful open-air festival.",
            category=categories['music'],
            date=today + timedelta(days=30),
            time=time(17, 0),
            venue="Omnisports Stadium Grounds, Yaoundé",
            capacity=800,
            ticket_price=4000.00,
            status='published',
            created_by=admin_user
        )

        event_music_hiphop = Event.objects.create(
            title="Cameroon Hip-Hop Summit",
            description="The biggest Hip-Hop event in Central Africa. Featuring Cameroonian rap stars, spoken word artists, beat producers, and emerging urban music talents from Douala to Bamenda.",
            category=categories['music'],
            date=today + timedelta(days=40),
            time=time(20, 0),
            venue="Arena Douala, Douala",
            capacity=600,
            ticket_price=7500.00,
            status='published',
            created_by=admin_user
        )

        event_music_afrobeats = Event.objects.create(
            title="Afrobeats Night Buea",
            description="Groove to the hottest Afrobeats hits in the Mountain City. A night packed with popular Afrobeats DJs and live artiste performances at the foot of Mount Fako.",
            category=categories['music'],
            date=today + timedelta(days=11),
            time=time(21, 0),
            venue="Great Soppo Community Hall, Buea",
            capacity=300,
            ticket_price=5000.00,
            status='published',
            created_by=admin_user
        )

        event_music_jazz_kribi = Event.objects.create(
            title="Kribi Beach Jazz Festival",
            description="Experience the magic of jazz under the tropical sky of Kribi. International and local jazz musicians perform on the famous white-sand beach with the Atlantic Ocean as a backdrop.",
            category=categories['music'],
            date=today + timedelta(days=45),
            time=time(16, 0),
            venue="Kribi Beach Resort, Kribi",
            capacity=400,
            ticket_price=8000.00,
            status='published',
            created_by=admin_user
        )

        event_music_concert = Event.objects.create(
            title="Locko & Friends Mega Concert",
            description="A star-studded mega concert headlined by Cameroonian R&B icon Locko. Special guest performances from top local and international artists. One of the biggest shows of the year.",
            category=categories['music'],
            date=today + timedelta(days=55),
            time=time(19, 30),
            venue="Palais des Congrès, Yaoundé",
            capacity=2000,
            ticket_price=15000.00,
            status='published',
            created_by=admin_user
        )

        # ============================
        # TECH EVENTS
        # ============================

        event2 = Event.objects.create(
            title="Silicon Mountain Tech Summit 2026",
            description="The premier tech conference in Central Africa bringing together developers, designers, and tech hub founders. Discussions on AI, FinTech, and regional connectivity.",
            category=categories['tech'],
            date=today + timedelta(days=25),
            time=time(9, 0),
            venue="Chariot Hotel Conference Hall, Buea",
            capacity=100,
            ticket_price=5000.00,
            status='published',
            created_by=admin_user
        )

        event7 = Event.objects.create(
            title="COLTECH HACKATHON 2026",
            description="An intensive 48-hour collaborative programming challenge at the College of Technology (COLTECH), University of Bamenda. Students design and build innovative tech solutions for real-world Cameroonian problems. Prizes and internship opportunities await the top teams.",
            category=categories['tech'],
            date=today + timedelta(days=12),
            time=time(9, 0),
            venue="COLTECH Campus, University of Bamenda",
            capacity=80,
            ticket_price=0.00,
            status='published',
            created_by=admin_user
        )

        event8 = Event.objects.create(
            title="NAHPI HACKATHON 2026",
            description="The National Higher Polytechnic Institute (NAHPI) Hackathon. Focuses on engineering, hardware-software integration, IoT solutions, and creative digital innovations. A 36-hour challenge open to all UBa engineering students.",
            category=categories['tech'],
            date=today + timedelta(days=18),
            time=time(8, 30),
            venue="NAHPI Building, University of Bamenda",
            capacity=100,
            ticket_price=0.00,
            status='published',
            created_by=admin_user
        )

        event11 = Event.objects.create(
            title="Frontend Dev Masterclass",
            description="Master modern Frontend Development. Build premium, highly responsive user interfaces with React, CSS Variables, animations, and accessibility best practices. Hands-on projects and mentorship from industry professionals.",
            category=categories['tech'],
            date=today + timedelta(days=14),
            time=time(10, 0),
            venue="Silicon Mountain Hub, Buea",
            capacity=60,
            ticket_price=2000.00,
            status='published',
            created_by=admin_user
        )

        event12 = Event.objects.create(
            title="Backend Dev Bootcamp",
            description="A deep dive into building scalable and secure backend architectures. Hands-on coding using Django, PostgreSQL, REST API frameworks, and cloud deployment. Ideal for intermediate developers looking to level up.",
            category=categories['tech'],
            date=today + timedelta(days=15),
            time=time(14, 0),
            venue="Silicon Mountain Hub, Buea",
            capacity=60,
            ticket_price=2500.00,
            status='published',
            created_by=admin_user
        )

        event_tech_ai = Event.objects.create(
            title="AI & Machine Learning Workshop",
            description="A hands-on workshop exploring the fundamentals of Artificial Intelligence and Machine Learning. Learn Python for ML, build predictive models, and explore how AI is transforming Africa's digital landscape.",
            category=categories['tech'],
            date=today + timedelta(days=20),
            time=time(9, 0),
            venue="FNB Building, University of Bamenda",
            capacity=50,
            ticket_price=3000.00,
            status='published',
            created_by=admin_user
        )

        event_tech_mobile = Event.objects.create(
            title="Mobile App Development Bootcamp",
            description="Build cross-platform mobile apps using React Native and Flutter. Learn how to deploy apps to Android and iOS stores, integrate payment APIs, and design beautiful mobile UI/UX.",
            category=categories['tech'],
            date=today + timedelta(days=28),
            time=time(10, 0),
            venue="Digit Hub, Douala",
            capacity=45,
            ticket_price=4000.00,
            status='published',
            created_by=admin_user
        )

        event_tech_cybersec = Event.objects.create(
            title="Cybersecurity Bootcamp Cameroon",
            description="Learn ethical hacking, penetration testing, network security, and digital forensics. This intensive bootcamp prepares participants for cybersecurity certifications like CEH and CompTIA Security+.",
            category=categories['tech'],
            date=today + timedelta(days=32),
            time=time(8, 0),
            venue="ISTDI Campus, Douala",
            capacity=40,
            ticket_price=5000.00,
            status='published',
            created_by=admin_user
        )

        event_tech_cloud = Event.objects.create(
            title="Cloud & DevOps Intensive",
            description="Master AWS, Google Cloud, Docker, Kubernetes, and CI/CD pipelines. A practical, project-based intensive for developers who want to build and deploy production-grade cloud infrastructure.",
            category=categories['tech'],
            date=today + timedelta(days=38),
            time=time(9, 30),
            venue="Coworking Yaoundé, Yaoundé",
            capacity=35,
            ticket_price=6000.00,
            status='published',
            created_by=admin_user
        )

        event_tech_data = Event.objects.create(
            title="Data Science & Analytics Symposium",
            description="Explore the power of data in driving business decisions in Africa. Sessions on Big Data, visualization with Power BI and Tableau, data pipelines, and real-world Cameroonian case studies.",
            category=categories['tech'],
            date=today + timedelta(days=50),
            time=time(10, 0),
            venue="Hilton Hotel Conference Room, Yaoundé",
            capacity=120,
            ticket_price=4500.00,
            status='published',
            created_by=admin_user
        )

        event_tech_web3 = Event.objects.create(
            title="Web3 & Blockchain Africa",
            description="Discover the potential of blockchain technology, DeFi, NFTs, and Web3 in the African economy. Learn about decentralized apps (dApps) and how to get started in the Web3 ecosystem.",
            category=categories['tech'],
            date=today + timedelta(days=60),
            time=time(11, 0),
            venue="Silicon Mountain Hub, Buea",
            capacity=80,
            ticket_price=2000.00,
            status='published',
            created_by=admin_user
        )

        event_tech_gamedev = Event.objects.create(
            title="Game Development Jam - UBa",
            description="A 72-hour game development marathon at the University of Bamenda. Build a working video game from scratch using Unity or Godot Engine. Open to all students and indie developers.",
            category=categories['tech'],
            date=today + timedelta(days=16),
            time=time(8, 0),
            venue="COLTECH Main Hall, University of Bamenda",
            capacity=60,
            ticket_price=0.00,
            status='published',
            created_by=admin_user
        )

        # ============================
        # SPORTS EVENTS
        # ============================

        event3 = Event.objects.create(
            title="Coupe du Cameroun Final Gala Match",
            description="Experience the historic final of the Coupe du Cameroun. A thrilling match between top division football clubs under the presence of national sports figures.",
            category=categories['sports'],
            date=today + timedelta(days=8),
            time=time(15, 30),
            venue="Stade Omnisports Ahmadou Ahidjo, Yaoundé",
            capacity=400,
            ticket_price=2500.00,
            status='published',
            created_by=admin_user
        )

        event_sports_marathon = Event.objects.create(
            title="Mt. Cameroon Race of Hope 2026",
            description="One of Africa's most prestigious mountain races. Runners from across the globe race up and down the 4,095m active volcano, Mount Cameroon. A test of endurance, spirit, and community.",
            category=categories['sports'],
            date=today + timedelta(days=35),
            time=time(7, 0),
            venue="Molyko Stadium, Buea",
            capacity=1000,
            ticket_price=0.00,
            status='published',
            created_by=admin_user
        )

        event_sports_basketball = Event.objects.create(
            title="Cameroon 3x3 Basketball League Finals",
            description="The electrifying national 3x3 basketball championship final. Watch elite street ballers compete for the national title in an action-packed afternoon of hoops and entertainment.",
            category=categories['sports'],
            date=today + timedelta(days=13),
            time=time(14, 0),
            venue="Multipurpose Sports Complex, Bamenda",
            capacity=300,
            ticket_price=1500.00,
            status='published',
            created_by=admin_user
        )

        event_sports_swim = Event.objects.create(
            title="Cameroon Aquatics Championship",
            description="National swimming and aquatics competitions across multiple categories. Young swimmers from all 10 regions compete for national glory and the chance to represent Cameroon internationally.",
            category=categories['sports'],
            date=today + timedelta(days=42),
            time=time(9, 0),
            venue="Olympic Swimming Pool, Yaoundé",
            capacity=200,
            ticket_price=1000.00,
            status='published',
            created_by=admin_user
        )

        # ============================
        # ARTS & CULTURE EVENTS
        # ============================

        event4 = Event.objects.create(
            title="Limbe Cultural Arts & Crafts Exhibition",
            description="Discover traditional woodcarving, authentic grassfields outfits, and local artistic paintings. An interactive workshop with Cameroonian master artisans.",
            category=categories['arts'],
            date=today + timedelta(days=10),
            time=time(10, 0),
            venue="Limbe Botanical Garden Hall, Limbe",
            capacity=4,
            ticket_price=1500.00,
            status='published',
            created_by=admin_user
        )

        event_arts_photo = Event.objects.create(
            title="Cameroon Photography Showcase",
            description="A curated exhibition of powerful photographs documenting the beauty, culture, struggles, and triumphs of Cameroonian life. Open to professional and amateur photographers nationwide.",
            category=categories['arts'],
            date=today + timedelta(days=17),
            time=time(11, 0),
            venue="National Museum of Cameroon, Yaoundé",
            capacity=100,
            ticket_price=2000.00,
            status='published',
            created_by=admin_user
        )

        event_arts_film = Event.objects.create(
            title="Nollywood & Camerwood Film Festival",
            description="A celebration of African cinema! Screenings of award-winning Cameroonian short films, feature films, and a live Q&A with local filmmakers. Discover stories told from an authentic African perspective.",
            category=categories['arts'],
            date=today + timedelta(days=24),
            time=time(14, 0),
            venue="CineJaune Cinema, Douala",
            capacity=180,
            ticket_price=3500.00,
            status='published',
            created_by=admin_user
        )

        event_arts_dance = Event.objects.create(
            title="Traditional Dance Extravaganza",
            description="A spectacular showcase of Cameroon's most vibrant traditional dances from the Bali Nyonga, Bamiléké, and Sawa peoples. A colorful pageant of costumes, drums, and cultural pride.",
            category=categories['arts'],
            date=today + timedelta(days=33),
            time=time(15, 0),
            venue="CRTV Grounds, Yaoundé",
            capacity=350,
            ticket_price=2500.00,
            status='published',
            created_by=admin_user
        )

        # ============================
        # BUSINESS EVENTS
        # ============================

        event5 = Event.objects.create(
            title="Sawa Cultural Gala & Dinner",
            description="An executive business networking dinner celebrating coastal culture, featuring business discussions, mockups of Kribi Deep Seaport investments, and traditional music.",
            category=categories['business'],
            date=today + timedelta(days=35),
            time=time(19, 0),
            venue="Kribi Down Beach Resort, Kribi",
            capacity=60,
            ticket_price=0.00,
            status='published',
            created_by=admin_user
        )

        event6 = Event.objects.create(
            title="Bamenda Young Entrepreneurs Seminar",
            description="A workshop focused on startup grants, business model validation, and agricultural entrepreneurship in the North-West region.",
            category=categories['business'],
            date=today + timedelta(days=20),
            time=time(11, 0),
            venue="Alliance Française, Bamenda",
            capacity=50,
            ticket_price=2000.00,
            status='draft',
            created_by=admin_user
        )

        event_biz_invest = Event.objects.create(
            title="Cameroon Investment Forum 2026",
            description="A high-level forum connecting international investors, government officials, and Cameroonian entrepreneurs. Focus areas include agriculture, digital economy, renewable energy, and tourism.",
            category=categories['business'],
            date=today + timedelta(days=45),
            time=time(8, 30),
            venue="Hilton Hotel, Yaoundé",
            capacity=200,
            ticket_price=25000.00,
            status='published',
            created_by=admin_user
        )

        event_biz_women = Event.objects.create(
            title="Women in Business Summit Douala",
            description="Empowering female entrepreneurs across Cameroon. Panel discussions, mentorship sessions, and pitch competitions celebrating the growing force of women-led businesses in Central Africa.",
            category=categories['business'],
            date=today + timedelta(days=27),
            time=time(9, 0),
            venue="Akwa Palace Hotel, Douala",
            capacity=150,
            ticket_price=5000.00,
            status='published',
            created_by=admin_user
        )

        event_biz_agri = Event.objects.create(
            title="Agri-Tech & Food Innovation Expo",
            description="Showcasing the future of agriculture and food processing in Cameroon. Exhibitors present smart farming tools, post-harvest technologies, and food packaging innovations for the African market.",
            category=categories['business'],
            date=today + timedelta(days=52),
            time=time(10, 0),
            venue="Palais des Congrès, Yaoundé",
            capacity=300,
            ticket_price=3000.00,
            status='published',
            created_by=admin_user
        )

        # ============================
        # EDUCATION EVENTS
        # ============================

        event_edu_career = Event.objects.create(
            title="UBa Career & Internship Fair 2026",
            description="Connect with top employers, multinationals, and NGOs operating in Cameroon. Bring your CV and explore internship, graduate trainee, and full-time job opportunities across multiple sectors.",
            category=categories['education'],
            date=today + timedelta(days=9),
            time=time(9, 0),
            venue="University of Bamenda Main Campus",
            capacity=500,
            ticket_price=0.00,
            status='published',
            created_by=admin_user
        )

        event_edu_stem = Event.objects.create(
            title="STEM for Girls Camp",
            description="A week-long immersive STEM program designed to inspire young girls aged 14-18 to pursue careers in Science, Technology, Engineering, and Mathematics. Fully sponsored by partner NGOs.",
            category=categories['education'],
            date=today + timedelta(days=21),
            time=time(8, 0),
            venue="GBHS Bamenda, Bamenda",
            capacity=80,
            ticket_price=0.00,
            status='published',
            created_by=admin_user
        )

        event_edu_debate = Event.objects.create(
            title="Inter-University Debate Championship",
            description="The finest student debaters from UBa, UY1, UYI, and UDs clash in a high-stakes debate tournament. Topics cover governance, technology, and socio-economic transformation in Africa.",
            category=categories['education'],
            date=today + timedelta(days=26),
            time=time(10, 0),
            venue="Amphitheatre, University of Bamenda",
            capacity=200,
            ticket_price=500.00,
            status='published',
            created_by=admin_user
        )

        # ============================
        # GAMING & ESPORTS EVENTS
        # ============================

        event_gaming_fifa = Event.objects.create(
            title="FIFA 25 eSports Championship",
            description="Cameroon's biggest FIFA video game tournament! 64 players battle head-to-head for the national champion title and cash prizes. Stream it live on Twitch and YouTube.",
            category=categories['gaming'],
            date=today + timedelta(days=6),
            time=time(12, 0),
            venue="Game Arena, Douala",
            capacity=64,
            ticket_price=1000.00,
            status='published',
            created_by=admin_user
        )

        event_gaming_lan = Event.objects.create(
            title="LAN Party Buea - Night of Legends",
            description="An epic overnight LAN party featuring CS2, League of Legends, and Valorant tournaments. Bring your setup or rent a rig on-site. Food, drinks, and prizes available throughout the night.",
            category=categories['gaming'],
            date=today + timedelta(days=19),
            time=time(18, 0),
            venue="Silicon Mountain Hub Gaming Lounge, Buea",
            capacity=100,
            ticket_price=2500.00,
            status='published',
            created_by=admin_user
        )

        # ============================
        # HEALTH & WELLNESS EVENTS
        # ============================

        event_health_run = Event.objects.create(
            title="Douala Health & Wellness Run 5K/10K",
            description="Join thousands of participants in a community fun run through the streets of Douala. Promotes healthy living, mental wellness, and corporate social responsibility. All fitness levels welcome.",
            category=categories['health'],
            date=today + timedelta(days=3),
            time=time(6, 30),
            venue="Wouri Bridge Start Line, Douala",
            capacity=2000,
            ticket_price=1000.00,
            status='published',
            created_by=admin_user
        )

        event_health_yoga = Event.objects.create(
            title="Sunrise Yoga at Mount Fako",
            description="A serene and rejuvenating yoga session at the base of Mount Cameroon as the sun rises over Buea. Ideal for beginners and advanced practitioners seeking mindfulness and natural beauty.",
            category=categories['health'],
            date=today + timedelta(days=4),
            time=time(5, 30),
            venue="Buea Town Square, Buea",
            capacity=50,
            ticket_price=2000.00,
            status='published',
            created_by=admin_user
        )

        self.stdout.write("-> Seeded 30+ events across Music, Tech, Sports, Arts, Business, Education, Gaming, and Health categories")

        # 5. Seed Bookings
        self.stdout.write("Seeding purchase transactions...")
        users_pool = [attendee1, attendee2, attendee3, attendee4, attendee5]

        # Fill Limbe Art Exhibition (capacity 4) to make it sold out
        for idx, user in enumerate(users_pool[:4]):
            booking = Booking.objects.create(user=user, event=event4, status='confirmed', payment_status='paid')
            Ticket.objects.create(booking=booking, event=event4)

        # Mboa Jazz bookings
        for user in [attendee1, attendee2]:
            booking = Booking.objects.create(user=user, event=event1, status='confirmed', payment_status='paid')
            Ticket.objects.create(booking=booking, event=event1)

        # Tech Summit bookings
        booking = Booking.objects.create(user=attendee2, event=event2, status='confirmed', payment_status='paid')
        Ticket.objects.create(booking=booking, event=event2)

        # Coupe du Cameroun bookings
        booking = Booking.objects.create(user=attendee3, event=event3, status='confirmed', payment_status='paid')
        Ticket.objects.create(booking=booking, event=event3)

        # COLTECH Hackathon bookings
        for user in [attendee1, attendee3, attendee4]:
            booking = Booking.objects.create(user=user, event=event7, status='confirmed', payment_status='paid')
            Ticket.objects.create(booking=booking, event=event7)

        # NAHPI Hackathon bookings
        for user in [attendee2, attendee5]:
            booking = Booking.objects.create(user=user, event=event8, status='confirmed', payment_status='paid')
            Ticket.objects.create(booking=booking, event=event8)

        # Frontend Dev bookings
        for user in [attendee1, attendee4]:
            booking = Booking.objects.create(user=user, event=event11, status='confirmed', payment_status='paid')
            Ticket.objects.create(booking=booking, event=event11)

        # Backend Dev bookings
        booking = Booking.objects.create(user=attendee5, event=event12, status='confirmed', payment_status='paid')
        Ticket.objects.create(booking=booking, event=event12)

        # Abakwa Music Fest bookings
        for user in [attendee2, attendee3, attendee4]:
            booking = Booking.objects.create(user=user, event=event10, status='confirmed', payment_status='paid')
            Ticket.objects.create(booking=booking, event=event10)

        # Health Run bookings
        for user in users_pool:
            booking = Booking.objects.create(user=user, event=event_health_run, status='confirmed', payment_status='paid')
            Ticket.objects.create(booking=booking, event=event_health_run)

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully with Cameroon content!"))
