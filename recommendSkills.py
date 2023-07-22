def recommendSkills(data):
    recommended_skills = []
    ds_keyword = ['tensorflow', 'keras', 'pytorch',
                  'machine learning', 'deep Learning', 'streamlit']
    web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                   'javascript', 'angular js', 'c#', 'flask', 'mongodb', 'sql', 'mysql']
    android_keyword = ['android', 'android development',
                       'flutter', 'kotlin', 'xml', 'kivy']
    ios_keyword = ['ios', 'ios development',
                   'swift', 'cocoa', 'cocoa touch', 'xcode']
    uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes', 'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator',
                    'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro', 'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp', 'user research', 'user experience']

    for i in data['skills']:
        if i.lower() in ds_keyword:
            recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling', 'Data Mining', 'Clustering & Classification', 'Data Analytics',
                                  'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras', 'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', "Flask", 'Streamlit']
            break
        elif i.lower() in web_keyword:
            recommended_skills = ['React', 'Django', 'NodeJS', 'ReactJS', 'php', 'Magento', 'Wordpress', 'Javascript', 'AngularJS',
                                  'C#', 'Flask', 'SDK', 'SQL', 'Mongo DB', 'MERN STACK', 'MEAN Stack', 'ExpressJS', 'Bootstrap', 'TailwindCSS', 'Vanilla']
            break
        elif i.lower() in android_keyword:
            recommended_skills = ['Android', 'Android development', 'Flutter', 'Kotlin',
                                  'XML', 'Java', 'Kivy', 'GIT', 'SDK', 'SQLite', 'Firebase', 'Android Security']
            break
        elif i.lower() in ios_keyword:
            recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode',
                                  'Objective-C', 'SQLite', 'Plist', 'StoreKit', "UI-Kit", 'AV Foundation', 'Auto-Layout']
            break
        elif i.lower() in uiux_keyword:
            recommended_skills = ['UI', 'User Experience', 'Adobe XD', 'Figma', 'Zeplin', 'Prototyping', 'Wireframes', 'Storyframes',
                                  'Adobe Photoshop', 'Editing', 'Illustrator', 'After Effects', 'Premier Pro', 'Indesign', 'Wireframe', 'Solid', 'Grasp', 'User Research']
            break

    return recommended_skills
