package interfaces;

import java.awt.EventQueue;

import javax.swing.JFrame;
import java.awt.Window.Type;
import javax.swing.JLayeredPane;
import java.awt.BorderLayout;
import java.awt.CardLayout;
import javax.swing.JPanel;
import java.awt.Color;
import java.awt.FlowLayout;
import javax.swing.SpringLayout;
import javax.swing.JButton;
import javax.swing.GroupLayout;
import javax.swing.GroupLayout.Alignment;
import javax.swing.SwingConstants;
import javax.swing.LayoutStyle.ComponentPlacement;
import java.awt.event.ActionListener;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.net.URLConnection;
import java.awt.event.ActionEvent;
import javax.swing.JLabel;

public class GraphicalUserInterface {

	private JFrame mainWindow;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					GraphicalUserInterface window = new GraphicalUserInterface();
					window.mainWindow.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the application.
	 */
	public GraphicalUserInterface() {
		initialize();
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		mainWindow = new JFrame();
		mainWindow.setTitle("Application Title\r\n");
		mainWindow.setBounds(100, 100, 640, 360);
		mainWindow.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		JLayeredPane layeredPane = new JLayeredPane();
		mainWindow.getContentPane().add(layeredPane, BorderLayout.CENTER);
		layeredPane.setLayout(new CardLayout(0, 0));
		
		JPanel pnlDebug = new JPanel();
		layeredPane.add(pnlDebug, "name_505311722576200");
		
		JButton btnTestButton = new JButton("Test Button");
		btnTestButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				try {
					testAPI();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		});
		
		JButton btnNewButton_1 = new JButton("New button");
		
		JButton button_1 = new JButton("New button");
		
		JButton button_2 = new JButton("New button");
		
		JButton button_3 = new JButton("New button");
		
		JButton button_4 = new JButton("New button");
		
		JButton button_5 = new JButton("New button");
		
		JButton button_6 = new JButton("New button");
		
		JButton button_7 = new JButton("New button");
		GroupLayout gl_pnlDebug = new GroupLayout(pnlDebug);
		gl_pnlDebug.setHorizontalGroup(
			gl_pnlDebug.createParallelGroup(Alignment.TRAILING)
				.addGroup(gl_pnlDebug.createSequentialGroup()
					.addContainerGap(271, Short.MAX_VALUE)
					.addComponent(btnTestButton)
					.addGap(254))
				.addGroup(Alignment.LEADING, gl_pnlDebug.createSequentialGroup()
					.addGap(48)
					.addGroup(gl_pnlDebug.createParallelGroup(Alignment.LEADING)
						.addGroup(gl_pnlDebug.createSequentialGroup()
							.addComponent(button_4, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
							.addGap(18)
							.addComponent(button_5, GroupLayout.DEFAULT_SIZE, 97, Short.MAX_VALUE)
							.addGap(18)
							.addComponent(button_6, GroupLayout.DEFAULT_SIZE, 97, Short.MAX_VALUE)
							.addGap(18)
							.addComponent(button_7, GroupLayout.DEFAULT_SIZE, 97, Short.MAX_VALUE))
						.addGroup(gl_pnlDebug.createSequentialGroup()
							.addComponent(btnNewButton_1)
							.addGap(18)
							.addComponent(button_1)
							.addGap(18)
							.addComponent(button_2)
							.addGap(18)
							.addComponent(button_3)))
					.addGap(132))
		);
		gl_pnlDebug.setVerticalGroup(
			gl_pnlDebug.createParallelGroup(Alignment.LEADING)
				.addGroup(gl_pnlDebug.createSequentialGroup()
					.addGap(48)
					.addComponent(btnTestButton)
					.addGap(67)
					.addGroup(gl_pnlDebug.createParallelGroup(Alignment.BASELINE)
						.addComponent(btnNewButton_1)
						.addComponent(button_1)
						.addComponent(button_2)
						.addComponent(button_3))
					.addGap(51)
					.addGroup(gl_pnlDebug.createParallelGroup(Alignment.BASELINE)
						.addComponent(button_4, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
						.addComponent(button_5, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
						.addComponent(button_6, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
						.addComponent(button_7, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
					.addGap(72))
		);
		pnlDebug.setLayout(gl_pnlDebug);
		
		JPanel pnlMenu = new JPanel();
		layeredPane.add(pnlMenu, "name_438676044161400");
		
		JButton btnNewButton = new JButton("Join Game");
		
		JButton button = new JButton("Join Game");
		GroupLayout gl_pnlMenu = new GroupLayout(pnlMenu);
		gl_pnlMenu.setHorizontalGroup(
			gl_pnlMenu.createParallelGroup(Alignment.LEADING)
				.addGroup(Alignment.TRAILING, gl_pnlMenu.createSequentialGroup()
					.addGap(256)
					.addGroup(gl_pnlMenu.createParallelGroup(Alignment.TRAILING)
						.addComponent(button, Alignment.LEADING, GroupLayout.DEFAULT_SIZE, 91, Short.MAX_VALUE)
						.addComponent(btnNewButton, Alignment.LEADING, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
					.addGap(275))
		);
		gl_pnlMenu.setVerticalGroup(
			gl_pnlMenu.createParallelGroup(Alignment.LEADING)
				.addGroup(gl_pnlMenu.createSequentialGroup()
					.addGap(67)
					.addComponent(btnNewButton, GroupLayout.DEFAULT_SIZE, 25, Short.MAX_VALUE)
					.addPreferredGap(ComponentPlacement.UNRELATED)
					.addComponent(button, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
					.addGap(183))
		);
		pnlMenu.setLayout(gl_pnlMenu);
		
		JPanel pnlConfig = new JPanel();
		layeredPane.add(pnlConfig, "name_508871004246000");
		
		JLabel lblEntryWayTo = new JLabel("entry way to change encrypted sheets link if needed to be changed etc");
		pnlConfig.add(lblEntryWayTo);
		
		JPanel pnlGame = new JPanel();
		layeredPane.add(pnlGame, "name_438204157148300");
		pnlGame.setLayout(new BorderLayout(0, 0));
		
		JPanel panel_1 = new JPanel();
		FlowLayout flowLayout = (FlowLayout) panel_1.getLayout();
		panel_1.setBackground(Color.ORANGE);
		panel_1.setForeground(Color.BLACK);
		pnlGame.add(panel_1, BorderLayout.NORTH);
		
		JPanel panel_2 = new JPanel();
		panel_2.setBackground(Color.BLUE);
		pnlGame.add(panel_2, BorderLayout.WEST);
		
		JPanel panel_3 = new JPanel();
		panel_3.setBackground(Color.MAGENTA);
		pnlGame.add(panel_3, BorderLayout.CENTER);
		
		JPanel panel_4 = new JPanel();
		panel_4.setBackground(Color.GREEN);
		pnlGame.add(panel_4, BorderLayout.EAST);
		
		JPanel panel_5 = new JPanel();
		panel_5.setBackground(Color.RED);
		pnlGame.add(panel_5, BorderLayout.SOUTH);
	}
	
	public void testAPI() throws IOException {
		System.out.println("test API things:");
		
		URL url = new URL("API-LINK");
		URLConnection con = url.openConnection();
		InputStream in = con.getInputStream();
		String encoding = con.getContentEncoding();  // ** WRONG: should use "con.getContentType()" instead but it returns something like "text/html; charset=UTF-8" so this value must be parsed to extract the actual encoding
		encoding = encoding == null ? "UTF-8" : encoding;
		
		//String body = IOUtils.toString(in, encoding);
		
		ByteArrayOutputStream baos = new ByteArrayOutputStream();
		byte[] buf = new byte[8192];
		int len = 0;
		while ((len = in.read(buf)) != -1) {
		    baos.write(buf, 0, len);
		}
		String body = new String(baos.toByteArray(), encoding);
		
		
		System.out.println(body);
		
		
	}
}
